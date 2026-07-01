import uuid
from datetime import datetime
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Enterprise, Application, ApplicationFile, AIReview
from .serializers import (
    RegisterSerializer, LoginSerializer, EnterpriseSerializer,
    ApplicationListSerializer, ApplicationDetailSerializer, ApplicationCreateSerializer,
    ApplicationFileSerializer, AIReviewSerializer, ReviewSerializer,
)
from .ai_review import run_ai_review


# ==================== 注册 & 登录 ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """企业注册"""
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'enterprise_name': user.enterprise.enterprise_name,
            'credit_code': user.enterprise.credit_code,
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录（支持企业用户和管理员）"""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    from django.contrib.auth import authenticate
    user = authenticate(username=serializer.validated_data['username'],
                        password=serializer.validated_data['password'])
    if user is None:
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    user_data = {
        'id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
    }
    if hasattr(user, 'enterprise'):
        user_data['enterprise_name'] = user.enterprise.enterprise_name
        user_data['credit_code'] = user.enterprise.credit_code
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': user_data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """获取当前登录用户信息"""
    user = request.user
    try:
        enterprise = user.enterprise
        return Response({
            'id': user.id,
            'username': user.username,
            'enterprise': EnterpriseSerializer(enterprise).data,
        })
    except Enterprise.DoesNotExist:
        return Response({'id': user.id, 'username': user.username, 'is_staff': user.is_staff})


# ==================== 备案申请 ====================

class ApplicationViewSet(viewsets.ModelViewSet):
    """备案申请 CRUD"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 企业只能看到自己的申请，管理员可以看到所有
        if self.request.user.is_staff:
            return Application.objects.all()
        try:
            enterprise = self.request.user.enterprise
        except Enterprise.DoesNotExist:
            return Application.objects.none()
        return Application.objects.filter(applicant=enterprise)

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ApplicationCreateSerializer
        return ApplicationDetailSerializer

    def perform_create(self, serializer):
        enterprise = self.request.user.enterprise
        # 生成申请编号: GF + 年月日 + 4位随机
        date_str = datetime.now().strftime('%Y%m%d')
        random_suffix = uuid.uuid4().hex[:4].upper()
        application_no = f'GF{date_str}{random_suffix}'
        application = serializer.save(applicant=enterprise, application_no=application_no)
        # 创建 AI 预审记录
        AIReview.objects.get_or_create(application=application)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """提交申请（草稿 → 待审核）"""
        application = self.get_object()
        if application.status != 'draft':
            return Response({'error': '只有草稿状态的申请才能提交'}, status=status.HTTP_400_BAD_REQUEST)

        # 检查是否上传了所有必需文件
        required_types = ['contract', 'receiver_license', 'receiver_capacity',
                          'transporter_license', 'transporter_pledge', 'legal_id']
        uploaded_types = set(application.files.values_list('file_type', flat=True))
        missing = [t for t in required_types if t not in uploaded_types]
        if missing:
            return Response({'error': f'请上传所有必需材料，缺少：{", ".join(missing)}'},
                            status=status.HTTP_400_BAD_REQUEST)

        application.status = 'pending'
        application.save()

        # 异步触发 AI 预审（简化：同步调用）
        try:
            run_ai_review(application)
        except Exception:
            pass  # AI 预审失败不影响提交

        return Response({'status': 'ok', 'message': '申请已提交'})


    @action(detail=True, methods=['post'])
    def upload_file(self, request, pk=None):
        """上传附件"""
        application = self.get_object()
        if application.status not in ('draft', 'rejected'):
            return Response({'error': '当前状态不允许上传文件'}, status=status.HTTP_400_BAD_REQUEST)

        file_type = request.data.get('file_type')
        if file_type not in dict(ApplicationFile.FILE_TYPES):
            return Response({'error': '无效的文件类型'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': '请选择文件'}, status=status.HTTP_400_BAD_REQUEST)

        # 限制文件大小 10MB
        if file_obj.size > 10 * 1024 * 1024:
            return Response({'error': '文件大小不能超过 10MB'}, status=status.HTTP_400_BAD_REQUEST)

        # 删除同一类型的旧文件
        ApplicationFile.objects.filter(application=application, file_type=file_type).delete()

        app_file = ApplicationFile.objects.create(
            application=application,
            file_type=file_type,
            file=file_obj,
            original_name=file_obj.name,
        )
        return Response(ApplicationFileSerializer(app_file).data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['delete'], url_path='files/(?P<file_id>[^/.]+)')
    def delete_file(self, request, pk=None, file_id=None):
        """删除附件"""
        application = self.get_object()
        app_file = ApplicationFile.objects.filter(id=file_id, application=application).first()
        if not app_file:
            return Response({'error': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)
        app_file.file.delete(save=False)
        app_file.delete()
        return Response({'status': 'ok'})


    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """管理员审核（通过/驳回/完成）"""
        if not request.user.is_staff:
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)

        application = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        action_type = serializer.validated_data['action']
        comment = serializer.validated_data.get('comment', '')

        if action_type == 'approve':
            application.status = 'approved'
        elif action_type == 'reject':
            application.status = 'rejected'
        elif action_type == 'complete':
            application.status = 'completed'

        application.review_comment = comment
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save()

        return Response({'status': 'ok', 'message': '审核完成'})


    @action(detail=True, methods=['get'])
    def ai_review_result(self, request, pk=None):
        """获取 AI 预审结果"""
        application = self.get_object()
        if hasattr(application, 'ai_review'):
            return Response(AIReviewSerializer(application.ai_review).data)
        return Response({'status': 'pending', 'summary': 'AI预审尚未开始'})


# ==================== 统计接口（首页用） ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def stats(request):
    """首页统计数据"""
    total = Application.objects.count()
    completed = Application.objects.filter(status='completed').count()
    # 计算办结率
    finished = Application.objects.filter(status__in=['approved', 'completed']).count()
    rate = round(finished / total * 100, 1) if total > 0 else 0
    return Response({
        'total': total,
        'completed': completed,
        'completion_rate': rate,
    })
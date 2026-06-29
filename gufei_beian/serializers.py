from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Enterprise, Application, ApplicationFile, AIReview


# ==================== 注册 & 登录 ====================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    # 企业字段
    credit_code = serializers.CharField(max_length=18)
    enterprise_name = serializers.CharField(max_length=200)
    region = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=300)
    legal_person = serializers.CharField(max_length=50)
    legal_person_id = serializers.CharField(max_length=18)
    contact_person = serializers.CharField(max_length=50)
    contact_phone = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'credit_code', 'enterprise_name',
                  'region', 'address', 'legal_person', 'legal_person_id', 'contact_person', 'contact_phone']

    def validate(self, data):
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password': '两次输入的密码不一致'})
        if Enterprise.objects.filter(credit_code=data['credit_code']).exists():
            raise serializers.ValidationError({'credit_code': '该统一社会信用代码已被注册'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': '该用户名已存在'})
        return data

    def create(self, validated_data):
        enterprise_fields = {k: validated_data.pop(k) for k in [
            'credit_code', 'enterprise_name', 'region', 'address', 'legal_person',
            'legal_person_id', 'contact_person', 'contact_phone'
        ]}
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        Enterprise.objects.create(user=user, **enterprise_fields)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# ==================== 企业信息 ====================

class EnterpriseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Enterprise
        fields = ['id', 'username', 'credit_code', 'enterprise_name', 'region', 'address',
                  'legal_person', 'contact_person', 'contact_phone', 'status', 'created_at']


# ==================== 申请附件 ====================

class ApplicationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFile
        fields = ['id', 'file_type', 'file', 'original_name', 'uploaded_at']
        read_only_fields = ['original_name']

    def create(self, validated_data):
        validated_data['original_name'] = validated_data['file'].name
        return super().create(validated_data)


# ==================== AI 预审 ====================

class AIReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIReview
        fields = ['id', 'status', 'summary', 'score', 'issues', 'suggestions', 'created_at']


# ==================== 备案申请 ====================

class ApplicationListSerializer(serializers.ModelSerializer):
    """申请列表（简要信息）"""
    applicant_name = serializers.CharField(source='applicant.enterprise_name', read_only=True)
    ai_review_status = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'application_no', 'applicant_name', 'transfer_unit', 'receive_unit',
                  'waste_name', 'transfer_amount', 'status', 'ai_review_status', 'created_at']

    def get_ai_review_status(self, obj):
        if hasattr(obj, 'ai_review'):
            return obj.ai_review.status
        return None


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """申请详情"""
    applicant_name = serializers.CharField(source='applicant.enterprise_name', read_only=True)
    applicant_credit_code = serializers.CharField(source='applicant.credit_code', read_only=True)
    files = ApplicationFileSerializer(many=True, read_only=True)
    ai_review = AIReviewSerializer(read_only=True)
    review_comment = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """创建/更新申请"""
    class Meta:
        model = Application
        fields = [
            'transfer_unit', 'transfer_address', 'transfer_contact', 'transfer_phone',
            'receive_unit', 'receive_province', 'receive_address', 'receive_contact', 'receive_phone',
            'disposal_method', 'waste_name', 'waste_category', 'waste_code', 'transfer_amount',
            'waste_form', 'packaging', 'main_components', 'hazardous',
            'transport_unit', 'transport_method', 'transfer_start', 'transfer_end',
        ]


# ==================== 审核（管理员用） ====================

class ReviewSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=[('approve', '通过'), ('reject', '驳回'), ('complete', '备案完成')])
    comment = serializers.CharField(required=False, allow_blank=True, default='')
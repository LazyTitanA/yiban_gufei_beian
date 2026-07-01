from django.db import models
from django.contrib.auth.models import User


class Enterprise(models.Model):
    """企业信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='enterprise', verbose_name='用户账号')
    credit_code = models.CharField(max_length=18, unique=True, verbose_name='统一社会信用代码')
    enterprise_name = models.CharField(max_length=200, verbose_name='企业名称')
    region = models.CharField(max_length=50, verbose_name='所在地')
    address = models.CharField(max_length=300, verbose_name='详细地址')
    legal_person = models.CharField(max_length=50, verbose_name='法定代表人')
    legal_person_id = models.CharField(max_length=18, verbose_name='法定代表人身份证号')
    contact_person = models.CharField(max_length=50, verbose_name='联系人')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    status = models.CharField(
        max_length=20,
        choices=[('active', '正常'), ('disabled', '已禁用')],
        default='active',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '企业信息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.enterprise_name}（{self.credit_code}）'


class Application(models.Model):
    """备案申请表"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('reviewing', '审核中'),
        ('approved', '已通过'),
        ('rejected', '已驳回'),
        ('completed', '备案完成'),
    ]

    applicant = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='applications', verbose_name='申请企业')
    application_no = models.CharField(max_length=30, unique=True, verbose_name='申请编号')

    # 转移单位信息
    transfer_unit = models.CharField(max_length=200, verbose_name='转移单位名称')
    transfer_address = models.CharField(max_length=300, verbose_name='转移单位地址')
    transfer_contact = models.CharField(max_length=50, verbose_name='转移联系人')
    transfer_phone = models.CharField(max_length=20, verbose_name='转移联系电话')

    # 接收单位信息
    receive_unit = models.CharField(max_length=200, verbose_name='接收单位名称')
    receive_province = models.CharField(max_length=50, verbose_name='接收省份')
    receive_address = models.CharField(max_length=300, verbose_name='接收单位地址')
    receive_contact = models.CharField(max_length=50, verbose_name='接收联系人')
    receive_phone = models.CharField(max_length=20, verbose_name='接收联系电话')
    disposal_method = models.CharField(max_length=50, verbose_name='处置方式')

    # 固体废物信息
    waste_name = models.CharField(max_length=200, verbose_name='废物名称')
    waste_category = models.CharField(max_length=50, verbose_name='废物类别')
    waste_code = models.CharField(max_length=50, verbose_name='废物代码')
    transfer_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='转移数量（吨）')
    waste_form = models.CharField(max_length=50, verbose_name='形态')
    packaging = models.CharField(max_length=200, verbose_name='包装方式')
    main_components = models.CharField(max_length=500, blank=True, default='', verbose_name='主要成分')
    hazardous = models.CharField(max_length=500, blank=True, default='', verbose_name='危险特性')

    # 运输信息
    transport_unit = models.CharField(max_length=200, verbose_name='运输单位')
    transport_method = models.CharField(max_length=50, verbose_name='运输方式')
    transfer_start = models.DateField(verbose_name='转移期限（起）')
    transfer_end = models.DateField(verbose_name='转移期限（止）')

    # 状态与审核
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    review_comment = models.TextField(blank=True, default='', verbose_name='审核意见')
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviews', verbose_name='审核人')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '备案申请'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.application_no} - {self.transfer_unit}'

    @property
    def file_count(self):
        return self.files.count()


class ApplicationFile(models.Model):
    """申请附件"""
    FILE_TYPES = [
        ('contract', '委托合同'),
        ('receiver_license', '接收方营业执照'),
        ('receiver_capacity', '接收方处置能力证明'),
        ('transporter_license', '运输方资质证明'),
        ('transporter_pledge', '运输方污染防治承诺书'),
        ('legal_id', '法人身份证明'),
        ('authorization', '授权委托书'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='files', verbose_name='所属申请')
    file_type = models.CharField(max_length=50, choices=FILE_TYPES, verbose_name='文件类型')
    file = models.FileField(upload_to='applications/%Y/%m/', verbose_name='文件')
    original_name = models.CharField(max_length=300, verbose_name='原始文件名')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '申请附件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.get_file_type_display()} - {self.original_name}'


class AIReview(models.Model):
    """AI 预审结果"""
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='ai_review', verbose_name='所属申请')
    status = models.CharField(
        max_length=20,
        choices=[('pending', '待处理'), ('passed', '预审通过'), ('failed', '预审不通过'), ('error', '处理异常')],
        default='pending',
        verbose_name='预审状态'
    )
    summary = models.TextField(blank=True, default='', verbose_name='预审摘要')
    score = models.IntegerField(null=True, blank=True, verbose_name='评分（0-100）')
    issues = models.JSONField(default=list, blank=True, verbose_name='发现的问题')
    suggestions = models.JSONField(default=list, blank=True, verbose_name='修改建议')
    raw_response = models.TextField(blank=True, default='', verbose_name='AI原始返回')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = 'AI预审'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'AI预审 - {self.application.application_no}'


class SystemConfig(models.Model):
    """系统配置（单例）"""
    ai_auto_review_enabled = models.BooleanField(default=False, verbose_name='AI 自动预审开关')
    ai_peak_hours = models.CharField(
        max_length=200,
        default='09:00-12:00,14:00-18:00',
        verbose_name='高峰时段（避开不处理）',
        help_text='格式：HH:MM-HH:MM,HH:MM-HH:MM，使用北京时间'
    )

    class Meta:
        verbose_name = '⚙️ 系统配置（AI预审开关）'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '系统配置'

    @classmethod
    def get_config(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
from django.contrib import admin
from django.utils.html import format_html
from .models import Enterprise, Application, ApplicationFile, AIReview


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['enterprise_name', 'credit_code', 'region', 'contact_person', 'contact_phone', 'status', 'created_at']
    list_filter = ['status', 'region']
    search_fields = ['enterprise_name', 'credit_code', 'contact_person']
    readonly_fields = ['created_at']


class ApplicationFileInline(admin.TabularInline):
    model = ApplicationFile
    extra = 0
    readonly_fields = ['file_type', 'file', 'original_name', 'uploaded_at']
    can_delete = False


class AIReviewInline(admin.StackedInline):
    model = AIReview
    readonly_fields = ['status', 'summary', 'score', 'issues_display', 'suggestions_display', 'created_at']
    can_delete = False
    fieldsets = (
        ('预审结果', {'fields': ('status', 'score', 'summary')}),
        ('问题与建议', {'fields': ('issues_display', 'suggestions_display')}),
    )

    def issues_display(self, obj):
        if not obj.issues:
            return '-'
        return format_html('<br>'.join(f'• {i}' for i in obj.issues))
    issues_display.short_description = '问题列表'

    def suggestions_display(self, obj):
        if not obj.suggestions:
            return '-'
        return format_html('<br>'.join(f'• {i}' for i in obj.suggestions))
    suggestions_display.short_description = '修改建议'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_no', 'applicant_name', 'transfer_unit', 'receive_unit',
                    'waste_name', 'transfer_amount', 'status', 'ai_status', 'created_at']
    list_filter = ['status', 'receive_province', 'created_at']
    search_fields = ['application_no', 'transfer_unit', 'receive_unit', 'waste_name']
    readonly_fields = ['application_no', 'created_at', 'updated_at', 'reviewed_by', 'reviewed_at']
    inlines = [ApplicationFileInline, AIReviewInline]

    fieldsets = (
        ('基本信息', {'fields': ('application_no', 'applicant', 'status', 'created_at', 'updated_at')}),
        ('转移单位信息', {'fields': ('transfer_unit', 'transfer_address', 'transfer_contact', 'transfer_phone')}),
        ('接收单位信息', {'fields': ('receive_unit', 'receive_province', 'receive_address', 'receive_contact', 'receive_phone', 'disposal_method')}),
        ('固体废物信息', {'fields': ('waste_name', 'waste_category', 'waste_code', 'transfer_amount', 'waste_form', 'packaging', 'main_components', 'hazardous')}),
        ('运输信息', {'fields': ('transport_unit', 'transport_method', 'transfer_start', 'transfer_end')}),
        ('审核信息', {'fields': ('review_comment', 'reviewed_by', 'reviewed_at')}),
    )

    def applicant_name(self, obj):
        return obj.applicant.enterprise_name
    applicant_name.short_description = '申请企业'

    def ai_status(self, obj):
        if hasattr(obj, 'ai_review'):
            status_map = {'pending': '⏳', 'passed': '✅', 'failed': '❌', 'error': '⚠️'}
            return format_html('{} {}', status_map.get(obj.ai_review.status, '?'), obj.ai_review.get_status_display())
        return '-'
    ai_status.short_description = 'AI预审'

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            obj.reviewed_by = request.user
            from django.utils import timezone
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(ApplicationFile)
class ApplicationFileAdmin(admin.ModelAdmin):
    list_display = ['application', 'file_type', 'original_name', 'uploaded_at']
    list_filter = ['file_type']


@admin.register(AIReview)
class AIReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'status', 'score', 'created_at']
    list_filter = ['status']
    readonly_fields = ['created_at']
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils import timezone
from .models import Enterprise, Application, ApplicationFile, AIReview, SystemConfig


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['enterprise_name', 'credit_code', 'region', 'contact_person', 'contact_phone', 'status', 'created_at']
    list_filter = ['status', 'region']
    search_fields = ['enterprise_name', 'credit_code', 'contact_person']
    readonly_fields = ['created_at']


class ApplicationFileInline(admin.TabularInline):
    model = ApplicationFile
    extra = 0
    readonly_fields = ['file_type', 'file_link', 'original_name', 'file_size_display', 'uploaded_at']
    can_delete = False

    def file_link(self, obj):
        if obj and obj.file:
            return format_html(
                '<a href="{}" target="_blank" style="color:#1B3A5C;text-decoration:underline;font-weight:bold;">📎 {}</a>',
                obj.file.url,
                obj.original_name or '下载查看'
            )
        return '-'
    file_link.short_description = '文件下载'
    file_link.allow_tags = True

    def file_size_display(self, obj):
        if obj and obj.file:
            try:
                size = obj.file.size
                if size < 1024:
                    return f'{size} B'
                elif size < 1024 * 1024:
                    return f'{size/1024:.1f} KB'
                else:
                    return f'{size/1024/1024:.1f} MB'
            except Exception:
                return '-'
        return '-'
    file_size_display.short_description = '文件大小'


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
                    'waste_name', 'transfer_amount', 'status', 'ai_status', 'created_at', 'ai_review_btn']
    list_filter = ['status', 'receive_province', 'created_at']
    search_fields = ['application_no', 'transfer_unit', 'receive_unit', 'waste_name']
    readonly_fields = ['application_no', 'created_at', 'updated_at', 'reviewed_by', 'reviewed_at', 'files_summary']
    inlines = [ApplicationFileInline, AIReviewInline]
    actions = ['run_ai_review_selected']

    fieldsets = (
        ('基本信息', {'fields': ('application_no', 'applicant', 'status', 'created_at', 'updated_at')}),
        ('转移单位信息', {'fields': ('transfer_unit', 'transfer_address', 'transfer_contact', 'transfer_phone')}),
        ('接收单位信息', {'fields': ('receive_unit', 'receive_province', 'receive_address', 'receive_contact', 'receive_phone', 'disposal_method')}),
        ('固体废物信息', {'fields': ('waste_name', 'waste_category', 'waste_code', 'transfer_amount', 'waste_form', 'packaging', 'main_components', 'hazardous')}),
        ('运输信息', {'fields': ('transport_unit', 'transport_method', 'transfer_start', 'transfer_end')}),
        ('附件材料一览', {'fields': ('files_summary',), 'classes': ('collapse',)}),
        ('审核信息', {'fields': ('review_comment', 'reviewed_by', 'reviewed_at')}),
    )

    def applicant_name(self, obj):
        return obj.applicant.enterprise_name
    applicant_name.short_description = '申请企业'

    def ai_status(self, obj):
        if hasattr(obj, 'ai_review') and obj.ai_review:
            status_map = {'pending': '⏳', 'passed': '✅', 'failed': '❌', 'error': '⚠️'}
            return format_html('{} {}', status_map.get(obj.ai_review.status, '?'), obj.ai_review.get_status_display())
        return '-'
    ai_status.short_description = 'AI预审'

    def ai_review_btn(self, obj):
        return format_html(
            '<a class="button" href="{}" onclick="return confirm(\'确认立即对该申请执行 AI 预审吗？\')">🤖 立即预审</a>',
            f'{obj.pk}/run_ai_review/'
        )
    ai_review_btn.short_description = 'AI预审操作'
    ai_review_btn.allow_tags = True

    def files_summary(self, obj):
        files = obj.files.all()
        if not files:
            return '（无附件）'
        html = '<div style="padding:10px 0;line-height:2;">'
        for f in files:
            try:
                size = f.file.size
                if size < 1024 * 1024:
                    size_str = f'{size/1024:.1f} KB'
                else:
                    size_str = f'{size/1024/1024:.1f} MB'
            except Exception:
                size_str = ''
            html += (
                f'<div style="margin-bottom:6px;padding:8px 12px;background:#f6f8fa;border-radius:4px;">'
                f'<b style="color:#333;">📎 {f.get_file_type_display()}</b> &nbsp; '
                f'<a href="{f.file.url}" target="_blank" style="color:#1B3A5C;text-decoration:underline;">'
                f'{f.original_name}</a> '
                f'<span style="color:#999;margin-left:8px;">{size_str}</span>'
                f'</div>'
            )
        html += '</div>'
        return format_html(html)
    files_summary.short_description = '附件材料一览'
    files_summary.allow_tags = True

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/run_ai_review/',
                self.admin_site.admin_view(self.run_ai_review_view),
                name='gufei_beian_application_run_ai_review',
            ),
        ]
        return custom_urls + urls

    def run_ai_review_view(self, request, pk):
        from django.shortcuts import redirect
        from django.urls import reverse
        from .ai_review import run_ai_review
        try:
            app = Application.objects.get(pk=pk)
            run_ai_review(app)
            self.message_user(request, f'AI 预审已完成：{app.application_no}', messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f'AI 预审失败：{str(e)}', messages.ERROR)
        return redirect(reverse('admin:gufei_beian_application_changelist'))

    def run_ai_review_selected(self, request, queryset):
        from .ai_review import run_ai_review
        count = 0
        for app in queryset:
            try:
                run_ai_review(app)
                count += 1
            except Exception as e:
                self.message_user(request, f'{app.application_no} 失败：{e}', messages.ERROR)
        self.message_user(request, f'已完成 {count} 个申请的 AI 预审', messages.SUCCESS)
    run_ai_review_selected.short_description = '🤖 批量执行 AI 预审'


@admin.register(ApplicationFile)
class ApplicationFileAdmin(admin.ModelAdmin):
    list_display = ['application', 'file_type', 'original_name', 'uploaded_at']
    list_filter = ['file_type']


@admin.register(AIReview)
class AIReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'status', 'score', 'created_at']
    list_filter = ['status']
    readonly_fields = ['created_at']


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'ai_auto_review_enabled', 'ai_peak_hours']
    list_display_links = ['id']

    def has_add_permission(self, request):
        return not SystemConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

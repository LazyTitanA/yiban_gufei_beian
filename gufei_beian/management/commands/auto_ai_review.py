from django.core.management.base import BaseCommand
from gufei_beian.models import Application, AIReview, SystemConfig
from gufei_beian.ai_review import run_ai_review
from gufei_beian.utils import is_peak_time
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '自动 AI 预审：处理所有待处理的申请（避开高峰时段）'

    def handle(self, *args, **options):
        config = SystemConfig.get_config()

        if not config.ai_auto_review_enabled:
            self.stdout.write('AI 自动预审未开启，跳过')
            return

        if is_peak_time(peak_str=config.ai_peak_hours):
            self.stdout.write('当前处于高峰时段，跳过 AI 预审')
            return

        pending = Application.objects.filter(status='pending')
        count = 0
        for app in pending:
            try:
                ai_review, _ = AIReview.objects.get_or_create(application=app)
                if ai_review.status == 'pending':
                    run_ai_review(app)
                    count += 1
                    self.stdout.write(f'  ✅ {app.application_no} 预审完成')
            except Exception as e:
                self.stderr.write(f'  ❌ {app.application_no} 预审失败: {e}')

        self.stdout.write(f'本次共处理 {count} 个申请')

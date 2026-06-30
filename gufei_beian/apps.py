from django.apps import AppConfig


class GufeiBeianConfig(AppConfig):
    name = 'gufei_beian'

    def ready(self):
        # 自动创建默认系统配置
        try:
            from .models import SystemConfig
            SystemConfig.get_config()
        except Exception:
            pass  # 数据库尚未就绪时跳过

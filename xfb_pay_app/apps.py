from django.apps import AppConfig

class XfbPayAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xfb_pay_app'

    def ready(self):
        try:
            # 导入信号处理器
            from . import signals
            # 记录应用启动
            import logging
            logger = logging.getLogger('xfb_pay_app')
            logger.info("应用启动完成")
        except ImportError as e:
            import logging
            logger = logging.getLogger('xfb_pay_app')
            logger.error(f"信号模块导入失败: {str(e)}")

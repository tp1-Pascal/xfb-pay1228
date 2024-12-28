from django.core.management.base import BaseCommand
import logging
import time

logger = logging.getLogger('xfb_pay_app')

class Command(BaseCommand):
    help = '记录系统状态'

    def handle(self, *args, **options):
        while True:
            logger.info("系统状态检查")
            time.sleep(300)  # 每5分钟记录一次 
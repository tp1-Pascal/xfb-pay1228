import sys
import django
import platform
import logging
import os

logger = logging.getLogger('xfb_pay_app')

def log_environment_info():
    """记录系统环境信息"""
    env_info = {
        'Python版本': sys.version,
        'Django版本': django.get_version(),
        'OS信息': platform.platform(),
        'CPU架构': platform.machine(),
        'Python路径': sys.executable,
        'Django设置模块': os.environ.get('DJANGO_SETTINGS_MODULE'),
        'DEBUG模式': os.environ.get('DEBUG', 'False'),
        '时区设置': os.environ.get('TZ', 'UTC'),
        '项目根目录': os.getcwd(),
    }
    
    logger.info("环境信息 - " + " | ".join(f"{k}:{v}" for k, v in env_info.items())) 
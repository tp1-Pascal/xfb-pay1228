#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
from datetime import datetime

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xfb_pay.settings')

    # 确保日志目录存在
    os.makedirs('logs', exist_ok=True)

    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename='logs/debug.log',
        filemode='a',
        encoding='utf-8'
    )

    logger = logging.getLogger(__name__)

    try:
        # 记录命令启动信息
        command = ' '.join(sys.argv)
        logger.info(f"执行命令: {command}")
        
        # 设置终端日志记录
        from xfb_pay_app.utils.terminal_logger import setup_terminal_logging
        setup_terminal_logging()
        
        # 记录启动时间
        start_time = datetime.now()
        logger.info(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
        
        # 记录结束时间
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"执行耗时: {duration:.2f}秒")
        
    except ImportError as exc:
        error_msg = f"导入错误: {str(exc)}"
        logger.error(error_msg)
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    except Exception as e:
        error_msg = f"执行错误: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise

if __name__ == '__main__':
    main()

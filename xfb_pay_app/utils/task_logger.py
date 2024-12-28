import logging
from functools import wraps
from datetime import datetime

logger = logging.getLogger('xfb_pay_app')

def log_scheduled_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_name = func.__name__
        start_time = datetime.now()
        
        logger.info(
            f"定时任务开始 - "
            f"任务:{task_name} "
            f"开始时间:{start_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(
                f"定时任务完成 - "
                f"任务:{task_name} "
                f"结束时间:{end_time.strftime('%Y-%m-%d %H:%M:%S')} "
                f"耗时:{duration:.2f}秒"
            )
            
            return result
            
        except Exception as e:
            logger.error(
                f"定时任务失败 - "
                f"任务:{task_name} "
                f"错误:{str(e)}",
                exc_info=True
            )
            raise
            
    return wrapper 
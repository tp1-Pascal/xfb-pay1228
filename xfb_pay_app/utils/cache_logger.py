from functools import wraps
import logging
import time

logger = logging.getLogger('xfb_pay_app')

def log_cache_operations(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        key = args[1] if len(args) > 1 else kwargs.get('key', 'unknown')
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(
                f"缓存操作 - "
                f"操作:{func.__name__} "
                f"键:{key} "
                f"耗时:{duration:.4f}秒 "
                f"结果:{'命中' if result is not None else '未命中'}"
            )
            return result
            
        except Exception as e:
            logger.error(
                f"缓存错误 - "
                f"操作:{func.__name__} "
                f"键:{key} "
                f"错误:{str(e)}"
            )
            raise
            
    return wrapper 
import logging
import time
from functools import wraps

logger = logging.getLogger('xfb_pay_app')

def log_view_access(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        
        # 记录请求信息
        logger.info(
            f"请求开始 - "
            f"视图:{view_func.__name__} "
            f"路径:{request.path} "
            f"方法:{request.method} "
            f"IP:{request.META.get('REMOTE_ADDR')} "
            f"用户:{request.user if request.user.is_authenticated else '匿名'}"
        )

        try:
            response = view_func(request, *args, **kwargs)
            
            # 记录响应信息
            execution_time = time.time() - start_time
            logger.info(
                f"请求完成 - "
                f"视图:{view_func.__name__} "
                f"状态码:{response.status_code} "
                f"耗时:{execution_time:.2f}秒"
            )
            
            return response
            
        except Exception as e:
            # 记录异常信息
            logger.error(
                f"请求异常 - "
                f"视图:{view_func.__name__} "
                f"异常:{str(e)}",
                exc_info=True
            )
            raise
            
    return wrapper 
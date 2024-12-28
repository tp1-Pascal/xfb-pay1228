import logging
import json
from functools import wraps

logger = logging.getLogger('xfb_pay_app')

def log_api_call(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # 记录请求信息
        request_data = {
            'method': request.method,
            'path': request.path,
            'query_params': request.GET.dict(),
            'body': request.body.decode() if request.body else None,
            'headers': dict(request.headers),
            'user': str(request.user),
            'ip': request.META.get('REMOTE_ADDR'),
        }
        
        logger.info(
            f"API请求 - "
            f"接口:{func.__name__} "
            f"数据:{json.dumps(request_data, ensure_ascii=False)}"
        )
        
        try:
            response = func(request, *args, **kwargs)
            
            # 记录响应信息
            response_data = {
                'status_code': response.status_code,
                'content': response.content.decode() if hasattr(response, 'content') else None,
                'headers': dict(response.headers),
            }
            
            logger.info(
                f"API响应 - "
                f"接口:{func.__name__} "
                f"数据:{json.dumps(response_data, ensure_ascii=False)}"
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"API错误 - "
                f"接口:{func.__name__} "
                f"错误:{str(e)}",
                exc_info=True
            )
            raise
            
    return wrapper 
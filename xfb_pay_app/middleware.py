import logging
import time

logger = logging.getLogger('xfb_pay_app')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        logger.info(f"收到请求 - PATH:{request.path}")
        response = self.get_response(request)
        duration = time.time() - start_time
        logger.info(f"请求结束 - PATH:{request.path} 耗时:{duration:.2f}秒")
        return response 
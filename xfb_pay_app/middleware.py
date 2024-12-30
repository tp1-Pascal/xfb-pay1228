import logging
import time

logger = logging.getLogger('django.request')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 记录请求开始
        start_time = time.time()
        
        # 记录请求信息
        logger.info(f'开始处理请求: {request.method} {request.path} from {request.META.get("REMOTE_ADDR")}')
        
        response = self.get_response(request)
        
        # 记录响应信息
        duration = time.time() - start_time
        logger.info(f'请求处理完成: {request.method} {request.path} - 状态码: {response.status_code} - 耗时: {duration:.2f}s')
        
        return response

    def process_exception(self, request, exception):
        # 记录异常信息
        logger.error(f'请求处理异常: {request.method} {request.path} - 错误: {str(exception)}')
        return None 
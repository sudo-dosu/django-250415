import time
import logging

logger = logging.getLogger(__name__)


class RequestTimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration = (time.perf_counter() - start) * 1000
        response['X-Request-Duration'] = f'{duration:.4f}ms'
        logger.info(f"{request.method} {request.path} took {duration:.4f}ms")
        return response

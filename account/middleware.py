
import threading

_thread_locals = threading.local()
def get_current_request():
    return getattr(_thread_locals, 'request', None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        request.session['ip_address'] = request.META.get('REMOTE_ADDR') 
        request.session.save()
        response = self.get_response(request)
        return response
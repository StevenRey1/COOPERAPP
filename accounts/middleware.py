import threading

# Create a shared thread-local storage for the whole application
thread_local = threading.local()

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Establecer la solicitud en el thread_local compartido
        thread_local.request = request
        response = self.get_response(request)
        return response

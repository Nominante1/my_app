from django.shortcuts import redirect

class RedirectMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.path == '/'):
            return redirect ('lab_3/password')
        response = self.get_response(request)
        return response
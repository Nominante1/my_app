from django.shortcuts import redirect

class RedirectMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.path == '/lab_4/'):
            return redirect ('sport_view')
        response = self.get_response(request)
        return response
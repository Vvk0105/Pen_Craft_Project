from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.template import TemplateDoesNotExist
from django.http import HttpResponseForbidden

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        return response
    
class HandleTemplateDoesNotExistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except TemplateDoesNotExist as e:
            if str(e) == 'registration/login.html':
                return redirect('login')  # Redirect to a custom error page
            raise
        return response
    
class StaffRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/staff/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect('/error-page/')  # Change to your error page
        return self.get_response(request)

class UserRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/user/'):
            if not request.user.is_authenticated or request.user.is_staff:
                return redirect('/error-page/')  # Change to your error page
        return self.get_response(request)
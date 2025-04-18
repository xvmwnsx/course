from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class BlockStudentAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            if hasattr(request.user, 'role') and request.user.role == 'student':
                return redirect(reverse('home'))

        return self.get_response(request)

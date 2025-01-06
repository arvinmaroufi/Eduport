from django.urls import reverse
from django.shortcuts import redirect


class RedirectAuthenticatedUserMiddleware:    # بعد از لاگین به این صفحات دسترسی ندارید
    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_urls = [
            reverse('AccountApp:sign-up'),
            reverse('AccountApp:sign-in'),
            reverse('AccountApp:forget-password'),
            reverse('AccountApp:verify-code'),
            reverse('AccountApp:reset-password'),
        ]

    def __call__(self, request):
        if request.user.is_authenticated and request.path in self.restricted_urls:
            return redirect('/')
        return self.get_response(request)

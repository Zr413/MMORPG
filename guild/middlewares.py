from django.shortcuts import redirect
from django.urls import reverse


class TwoFactorAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if not request.user.is_verified:
            # Пользователь должен подтвердить учётную запись
            return redirect(reverse('verify_otp'))
        return self.get_response(request)
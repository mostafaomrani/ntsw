from django.contrib.auth import get_user
from django.urls import resolve, Resolver404
from django.conf import settings
from django.utils.timezone import now
from django.urls import resolve, reverse
from django.shortcuts import redirect
from django.urls import resolve


class RedirectAnonymusUserToLogin:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        user = request.user
        if not user.is_authenticated:
            r = resolve(request.path_info)
            current_app_names = r.app_names
            current_url_name = r.url_name
            allowed_urls = ['zarinpal']
            allowed_apps = ['users']
            if not any(app in allowed_apps for app in current_app_names) and not (current_url_name in allowed_urls):
                return redirect('users:login')
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class RedirectAuthenticatedUserFromLoginToDashboar:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        user = request.user
        if user.is_authenticated:
            r = resolve(request.path_info)
            current_app_names = r.app_names
            current_url_name = r.url_name
            redirect_apps = ['users']
            if any(app in redirect_apps for app in current_app_names) and not current_url_name == 'logout':
                return redirect('dashboard:base_role_dashboard')
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class AuthRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            resolver_match = resolve(request.path_info)
            current_url_name = resolver_match.url_name or ""
            current_app_names = resolver_match.app_names or []
        except Resolver404:
            # مسیر ناشناخته → اجازه بده بره جلو تا 404 داده بشه
            return self.get_response(request)

        # مسیرهای عمومی بدون نیاز به احراز هویت
        public_url_names = ['login', 'logout', 'password_reset']
        public_apps = ['users', 'zarinpal', 'public']

        user = request.user

        # کاربر وارد نشده → محافظت از مسیرهای خصوصی
        if not user.is_authenticated:
            if current_url_name not in public_url_names and not any(app in public_apps for app in current_app_names):
                return redirect('users:login')

        # کاربر وارد شده → نباید به صفحه‌ی login یا signup دسترسی داشته باشه
        elif user.is_authenticated:
            if current_url_name in ['login', 'signup'] and any(app in ['users'] for app in current_app_names):
                return redirect('dashboard:base_role_dashboard')

        return self.get_response(request)


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            session_age = settings.SESSION_COOKIE_AGE  # مقدار تنظیم‌شده در settings.py
            if last_activity:
                elapsed_time = now().timestamp() - last_activity
                if elapsed_time > session_age:
                    request.session.flush()  # خروج از حساب کاربری
                else:
                    request.session.set_expiry(session_age)

            request.session['last_activity'] = now(
            ).timestamp()  # بروزرسانی زمان فعالیت

        return self.get_response(request)

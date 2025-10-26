from decouple import config
from persiantools.jdatetime import JalaliDate
from django.shortcuts import get_object_or_404
from users.models import Role, TraderRole

def request_protocol(request):
    has_ssl = config('HAS_SSL', cast=bool, default=True)
    if has_ssl:
        return {
            'protocol': 'https://'
        }
    return {
        'protocol': 'http://'
    }

def jalali_now(request):
    j_date = JalaliDate.today()
    return {
        'jalali_now': j_date.strftime("%A, %d %B %Y", locale="fa"),
    }

def session_cookie_age(request):    
    return {
        'session_cookie_age': config(
            'SESSION_COOKIE_AGE',
            cast=int
        )
    }

def user_roles(request):
    # اگر کاربر لاگین نکرده باشد، roles_data و trade_roles خالی برگردان
    if not request.user.is_authenticated:
        return {
            'roles_data': [],
            'trade_roles': []
        }

    # گرفتن نقش‌های کاربر
    roles = request.user.roles.all().order_by('id')

    try:
        br_role = Role.objects.get(code="br")
    except Role.DoesNotExist:
        br_role = None

    if br_role:
        # بذار br اول لیست باشه
        roles = [br_role] + [r for r in roles if r != br_role]

    # ایجاد roles_data با ترکیب title و activity_type
    roles_data = []
    for role in roles:
        trader_role = TraderRole.objects.filter(user=request.user, role=role).first()
        if trader_role:
            display_title = f"{role.title} - {trader_role.activity_type}"
        else:
            display_title = role.title
        roles_data.append({
            'code': role.code,
            'title': display_title
        })

    return {
        'roles_data': roles_data,
        'trade_roles': []
    }
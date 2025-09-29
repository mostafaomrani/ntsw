from decouple import config
from persiantools.jdatetime import JalaliDate
from decouple import config
from users.models import Role 

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
    roles = request.user.roles.all().order_by('id') if request.user.is_authenticated else []

    try:
        br_role = Role.objects.get(code="br")
    except Role.DoesNotExist:
        br_role = None

    if br_role:
        # بذار br اول لیست باشه
        roles = [br_role] + [r for r in roles if r != br_role]

    return {
        'roles_data': roles,
        'trade_roles' : []
    }
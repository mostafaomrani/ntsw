from django.contrib.messages import constants as messages
from pathlib import Path
from decouple import config, Csv

IS_DEVELOPMENT_ENVIRONMENT = config('IS_DEVELOPMENT_ENVIRONMENT', cast=bool)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=False)


ALLOWED_HOSTS = ['127.0.0.1', 'localhost','demo.pouyabehzadnia.com','185.63.113.238']

if not IS_DEVELOPMENT_ENVIRONMENT:
    CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv())
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', cast=bool, default=True)
SESSION_COOKIE_SECURE = config(
    'SESSION_COOKIE_SECURE',
    cast=bool,
    default=True
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS += [
    'widget_tweaks',
]

INSTALLED_APPS += [
    'users.apps.UsersConfig',
    'dashboard.apps.DashboardConfig',
    'upload_qualifications',
    # 'product_identifier.apps.ProductIdentifierConfig',
    'overseas_supplier.apps.OverseasSupplierConfig',
    'order_registration.apps.OrderRegistrationConfig',
    'currency_allocation.apps.CurrencyAllocationConfig',
    'currency_origin_determining.apps.CurrencyOriginDeterminingConfig',
    'extensions',
    'import_export',
    'apps.payments.apps.PaymentsConfig',
    'product_identifier',
    'shenase',
    'foreintrade',
    'production_operations'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE += [
    # 'dashboard.middleware.RedirectAnonymusUserToLogin',
    # 'dashboard.middleware.RedirectAuthenticatedUserFromLoginToDashboar',
    # 'dashboard.middleware.AuthRedirectMiddleware',


    # 'dashboard.middleware.SessionTimeoutMiddleware',
]
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.context_processors.request_protocol',
                'dashboard.context_processors.jalali_now',
                'dashboard.context_processors.session_cookie_age',
                'dashboard.context_processors.user_roles',
            ],

        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
database_engin = config('DATABASE_ENGINE')
if database_engin == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
elif database_engin == 'psql':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
        }

    }
else:
    raise Exception('SELECT a data bbase')
    exit()

    # Password validation
    # https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True
USE_L10N = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

if (IS_DEVELOPMENT_ENVIRONMENT):
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]
else:
    STATIC_ROOT = BASE_DIR / "static"

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.SmallAutoField'
AUTH_USER_MODEL = 'users.CustomUser'
SITE_ID = config('SITE_ID', cast=int)
LOGIN_REDIRECT_URL = 'dashboard:base_role_dashboard'
LOGIN_URL = 'users:login'
LOGOUT_REDIRECT_URL = 'users:login'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# SESSION_COOKIE_AGE = config(
# 'SESSION_COOKIE_AGE',
# cast=int
# )
# SESSION_EXPIRE_AT_BROWSER_CLOSE = config(
# 'SESSION_EXPIRE_AT_BROWSER_CLOSE',
# cast=bool,
# default=True
# )
if IS_DEVELOPMENT_ENVIRONMENT:

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]

    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    INTERNAL_IPS = [
        # ...
        # "127.0.0.1",
        # ...
    ]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "django.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "myproject.custom": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
MESSAGE_TAGS = {
    messages.DEBUG: 'alert alert-info alert-dismissible fase show',
    messages.INFO: 'alert alert-info alert-dismissible fase show',
    messages.SUCCESS: 'alert alert-success alert-dismissible fase show',
    messages.WARNING: 'alert alert-warning alert-dismissible fase show',
    messages.ERROR: 'alert alert-danger alert-dismissible fase show',
}


PAYMENT_GATEWAYS = [
    {
        'name': 'zarinpal',
        'module': 'zarinpal',
        'class': 'ZarinpalGateway',
        'display_name': 'زرین‌پال',
        'enabled': True,
        'logo': 'zarinpal.png',
        'url': 'payments:zarinpal_payment',
    },
    {
        'name': 'zibal',
        'module': 'zibal',
        'class': 'ZibalGateway',
        'display_name': 'زیبال',
        'enabled': False,
        'logo': 'zarinpal.png',
        'url': 'payments:zibal_payment',
    },

]

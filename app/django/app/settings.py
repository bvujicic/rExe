import os

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from yml_config  import Config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Config.from_yaml('config/config.yml')
env.to_env()


DEBUG = env('DJANGO_DEBUG', False)
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', '*').split()
SECRET_KEY = env('DJANGO_SECRET_KEY')

INTERNAL_IPS = ['127.0.0.1']

ADMINS = [
    (env('DJANGO_ADMIN_NAME'), env('DJANGO_ADMIN_EMAIL'))
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(env('DJANGO_DATABASE_BACKEND', 'sqlite3')),
        'NAME': env('DJANGO_DATABASE_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': env('DJANGO_DATABASE_USER'),
        'PASSWORD': env('DJANGO_DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# Cache
if env('DJANGO_REDIS_LOCATION'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env('DJANGO_REDIS_LOCATION'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'TIMEOUT': None
        }
    }


# Session
if env('DJANGO_REDIS_LOCATION'):
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


# Email
EMAIL_BACKEND = 'django.core.mail.backends.{}.EmailBackend'.format(env('DJANGO_EMAIL_BACKEND'))
DEFAULT_FROM_EMAIL = 'system@rExe'
EMAIL_HOST = env('DJANGO_EMAIL_HOST')
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Application definition
INSTALLED_APPS = [
    #'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rosetta',
    'web.apps.WebConfig'
]

# if DEBUG:
#     INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# if DEBUG:
#     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'resources', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Internationalization
LANGUAGE_CODE = 'hr'
LANGUAGES = (
    ('hr', _('hrvatski')),
    ('en', _('engleski'))
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TIME_ZONE = 'Europe/Zagreb'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'resources', 'static'),
]
STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_PATH')


# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_PATH')
FILE_UPLOAD_PERMISSIONS = 0o744

# Login
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('home')


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] [logger: %(name)s] [%(levelname)s] [%(module)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': "%(levelname)s %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': 'django.core.mail.backends.{}.EmailBackend'.format(env('DJANGO_EMAIL_BACKEND')),
            'level': 'ERROR',
            'include_html': True
        },
        'django': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024,
            'backupCount': 10,
            'filename': os.path.join(env('DJANGO_LOG_PATH', BASE_DIR), 'django.log'),
            'level': 'INFO',
            'formatter': 'verbose'
        },
        'web': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024,
            'backupCount': 10,
            'filename': os.path.join(env('DJANGO_LOG_PATH', BASE_DIR), 'web.log'),
            'level': 'INFO',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'web': {
            'handlers': ['web', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_IMPORTS = [
    'web.tasks'
]

# Custom
SUBPROCESS_TIMEOUT = 60 * 60
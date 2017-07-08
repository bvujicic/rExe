import os

import cloudinary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ.get = os.environ.get


DEBUG = os.environ.get('DJANGO_DEBUG', False)
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split()
SECRET_KEY = 'asdfsa'

INTERNAL_IPS = ['127.0.0.1']

ADMINS = [
    (os.environ.get('DJANGO_ADMIN_NAME'), os.environ.get('DJANGO_ADMIN_EMAIL'))
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(os.environ.get('DJANGO_DATABASE_BACKEND', 'sqlite3')),
        'NAME': os.environ.get('POSTGRES_DB', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# Cache
if os.environ.get('DJANGO_REDIS_LOCATION'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.environ.get('DJANGO_REDIS_LOCATION'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'TIMEOUT': None
        }
    }


# Session
if os.environ.get('DJANGO_REDIS_LOCATION'):
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


# Email
EMAIL_BACKEND = 'django.core.mail.backends.{}.EmailBackend'.format(os.environ.get('DJANGO_EMAIL_BACKEND'))
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Application definition
INSTALLED_APPS = [
    #'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    #'cloudinary',
    #'nucleus',
    'web'
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
LANGUAGE_CODE = 'hr_HR'

TIME_ZONE = 'Europe/Zagreb'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'resources', 'static'),
]
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'


# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_PATH')


# Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': "[%(asctime)s] [logger: %(name)s] [%(levelname)s] [%(module)s:%(lineno)s] %(message)s",
#             'datefmt': "%Y-%m-%d %H:%M:%S"
#         },
#         'simple': {
#             'format': "%(levelname)s %(message)s"
#         }
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'level': 'DEBUG',
#             'formatter': 'verbose'
#         },
#         'mail_admins': {
#             'class': 'django.utils.log.AdminEmailHandler',
#             'email_backend': 'django.core.mail.backends.{}.EmailBackend'.format(os.environ.get('DJANGO_EMAIL_BACKEND')),
#             'level': 'ERROR',
#             'include_html': True
#         },
#         'django': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'maxBytes': 1024 * 1024,
#             'backupCount': 10,
#             'filename': '/var/log/django.log',
#             'level': 'INFO',
#             'formatter': 'verbose'
#         },
#         'web': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'maxBytes': 1024 * 1024,
#             'backupCount': 10,
#             'filename': '/var/log/web.log',
#             'level': 'INFO',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['django', 'console'],
#             'level': 'INFO',
#             'propagate': False
#         },
#         'web': {
#             'handlers': ['web', 'console'],
#             'level': 'INFO',
#             'propagate': False
#         }
#     }
# }

# Cloudinary
cloudinary.config(
  cloud_name = os.environ.get('DJANGO_CLOUDINARY_CLOUD_NAME'),
  api_key = os.environ.get('DJANGO_CLOUDINARY_API_KEY'),
  api_secret = os.environ.get('DJANGO_CLOUDINARY_API_SECRET')
)

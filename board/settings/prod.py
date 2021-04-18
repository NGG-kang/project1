from .common import *

INSTALLED_APPS += [
    'storages',
]

DEBUG = os.environ.get('DEBUG') in ['1', 't', 'true', 'True']

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(',')

AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = ''
AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_REGION

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_SECURE_URLS = False       # use http instead of https
AWS_QUERYSTRING_AUTH = False

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_S3_ACCESS_KEY_ID = ''
AWS_S3_SECRET_ACCESS_KEY = ''

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

# Static Setting
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# Media Setting
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CHARSET = 'utf8'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "ERROR", "class": "logging.StreamHandler", }, },
    "loggers": {"django": {"handlers": ["console"], "level": "ERROR", }, },
}
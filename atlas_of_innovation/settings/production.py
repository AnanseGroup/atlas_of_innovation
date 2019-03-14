from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY_WARNING: don't use these keys in production
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = '6LdzuFAUAAAAAExNBiaezBVZMZQ-4FFh_tyLg1hR'
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(",") or \
                ["atlasenv.g3a3emn8g9.us-west-2.elasticbeanstalk.com",
				 ".atlasofinnovation.com"]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'
EMAIL_BACKEND = 'post_office.EmailBackend'
#use gmailserver
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'atlasofinnovation@gmail.com'
EMAIL_HOST_PASSWORD = '4tl4sofinnovation'
EMAIL_PORT = 587
POST_OFFICE = {
    'DEFAULT_PRIORITY': 'now'
}

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

# Assets
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")

STATIC_URL = '/static/'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
TEMPLATE_STRING_IF_INVALID="invalid field name"
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


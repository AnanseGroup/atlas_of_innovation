from .production import *

DEBUG = True

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

URL="staging.atlasofinnovation.com"
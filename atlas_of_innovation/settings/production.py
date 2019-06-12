from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Assets
STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")


STATIC_URL = '/static/'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
TEMPLATE_STRING_IF_INVALID="invalid field name"
EMAIL_BACKEND = 'post_office.EmailBackend'
#use sengrid
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

URL="atlasofinnovation.com"


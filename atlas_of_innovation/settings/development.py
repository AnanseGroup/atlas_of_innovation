from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l^o92!g+^lp459xkndhnc620hutn8lb%fueku1n4pxe+2vch1i'

# SECURITY_WARNING: don't use these keys in production 
RECAPTCHA_PUBLIC_KEY = '6Lf_uiQUAAAAALicrb1JbiITWdIdOTuQzIHnnodJ'
RECAPTCHA_PRIVATE_KEY = '6Lf_uiQUAAAAABHjt9ryEqxIOPTSMDeEQSrz7O-q'
NOCAPTCHA = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
'''
Django settings for scouts_kampvisum_api project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
'''

import os, logging, logging.config
from environs import Env


logger = logging.getLogger(__name__)

# https://stackoverflow.com/questions/53014435/why-is-logging-in-my-django-settings-py-ignored
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'filename': 'scouts-kampvisum.debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'scouts_auth': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
logging.config.dictConfig(LOGGING)


# Environment loading
env = Env()
env.read_env()

# Load the appropriate environment file
# In .env, define as only variable ENVIRONMENT
# Set it to 'development' or 'production' and define the appropriate variables
# in .env_development and .env_production
# Default: development
environments = [
    '.env.dev.local',
    '.env.dev',
    '.env.production'
]

environment_conf = env.str('ENVIRONMENT', default = None)
environment_loaded = False

if environment_conf:
    try:
        env=Env()
        env.read_env('.env.' + environment_conf)
        
        environment_loaded = True
        logger.debug('Environment file loaded: .env.' +  environment_conf)
    except Exception:
        logger.warn('WARN: Environment file .env.' + environment_conf,
               ' not found ! ' +
               'Defaulting to next configured default environment.')
    
    if not environment_loaded:
        for environment in environments:
            if environment == '.env.' + environment_conf:
                pass
            
            try:
                env = Env()
                env.read_env('.env.' + environment)
                
                logger.debug('Environment file loaded: .env.' + environment)
                environment_loaded = True
            except Exception:
                pass


def correct_url(issuer, url):
    if not url.startswith('http'):
        return issuer + url
    return url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
BASE_URL = env.str('BASE_URL', default = '/')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'scouts_auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'sqlmiddleware',
    'safedelete',
    'apps.base',
    'apps.scouts_camp_visums',
    'apps.scouts_camps',
    'apps.scouts_groups',
    'rest_framework',
    'django_filters',
    'drf_yasg2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'scouts_kampvisum_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'scouts_kampvisum_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': env.str('DBENGINE'),
        'NAME': env.str('DBNAME'),
        'USER': env.str('DBUSER'),
        'PASSWORD': env.str('DBPASSWORD'),
        'HOST': env.str('DBHOST'),
        'PORT': env.str('DBPORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
django_pw_validation = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': django_pw_validation + 'UserAttributeSimilarityValidator',
    },
    {
        'NAME': django_pw_validation + 'MinimumLengthValidator',
    },
    {
        'NAME': django_pw_validation + 'CommonPasswordValidator',
    },
    {
        'NAME': django_pw_validation + 'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# STATIC FILES (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = env.str('STATIC_ROOT')


# DEFAULT PRIMARY KEY FIELD TYPE
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'scouts_auth.oidc.InuitsOIDCAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'scouts_kampvisum_api.pagination.PageNumberPagination',
    'EXCEPTION_HANDLER':
        'apps.base.exceptions.exception_handler',
}


# EMAIL
# We are going to use anymail which maps multiple providers like sendinblue
# with default django mailing
# For more info see https://anymail.readthedocs.io/en/stable/esps/sendinblue/
EMAIL_BACKEND = 'anymail.backends.sendinblue.EmailBackend'

ANYMAIL = {
    'SENDINBLUE_API_KEY': '<API key here, get it from env file>',
}


# CORS
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST')


# OIDC
# @SEE https://mozilla-django-oidc.readthedocs.io/en/stable/
# PDF: https://mozilla-django-oidc.readthedocs.io/_/downloads/en/stable/pdf/
AUTH_USER_MODEL = 'scouts_auth.User'

AUTHENTICATION_BACKENDS = {
    'scouts_auth.oidc.InuitsOIDCAuthenticationBackend',
}
OIDC_OP_ISSUER = env.str('OIDC_OP_ISSUER')
# URL of your OpenID Connect provider authorization endpoint
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_OP_AUTHORIZATION_ENDPOINT
OIDC_OP_AUTHORIZATION_ENDPOINT = correct_url(
    OIDC_OP_ISSUER, env.str("OIDC_OP_AUTHORIZATION_ENDPOINT"))
# URL of your OpenID Connect provider token endpoint
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_OP_TOKEN_ENDPOINT
OIDC_OP_TOKEN_ENDPOINT = correct_url(
    OIDC_OP_ISSUER, env.str('OIDC_OP_TOKEN_ENDPOINT'))
# URL of your OpenID Connect provider userinfo endpoint
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_OP_USER_ENDPOINT
OIDC_OP_USER_ENDPOINT = correct_url(
    OIDC_OP_ISSUER, env.str('OIDC_OP_USER_ENDPOINT'))
# OpenID Connect client ID provided by your OP
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_CLIENT_ID
OIDC_RP_CLIENT_ID = env.str('OIDC_RP_CLIENT_ID')
# OpenID Connect client secret provided by your OP
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_CLIENT_SECRET
OIDC_RP_CLIENT_SECRET = env.str('OIDC_RP_CLIENT_SECRET')
# Controls whether the OpenID Connect client verifies the signature
# of the JWT tokens
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_VERIFY_JWT
OIDC_VERIFY_JWT = env.bool('OIDC_VERIFY_JWT', default = True)
# Controls whether the OpenID Connect client verifies the KID field
# of the JWT tokens
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_VERIFY_KID
OIDC_VERIFY_KID = env.bool('OIDC_VERIFY_KID', default = True)
# Controls whether the OpenID Connect client uses nonce verification
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_USE_NONCE
OIDC_USE_NONCE = env.bool('OIDC_USE_NONCE', default = True)
# Controls whether the OpenID Connect client verifies the SSL certificate of the OP responses
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_VERIFY_SSL
OIDC_VERIFY_SSL = env.bool('OIDC_VERIFY_SSL', default = True)
# Defines a timeout for all requests to the OpenID Connect provider
# (fetch JWS, retrieve JWT tokens, Userinfo Endpoint). The default is set to
# None which means the library will wait indefinitely. The time can be defined
# as seconds (integer). More information about possible configuration values,
# see Python requests:
# https://requests.readthedocs.io/en/master/user/quickstart/#timeouts
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_TIMEOUT
OIDC_TIMEOUT = env.str('OIDC_TIMEOUT', default = None)
# Defines a proxy for all requests to the OpenID Connect provider
# (fetch JWS, retrieve JWT tokens, Userinfo Endpoint). The default is set to
# None which means the library will not use a proxy and connect directly.
# For configuring a proxy check the Python requests documentation:
# https://requests.readthedocs.io/en/master/user/advanced/#proxies
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_PROXY
OIDC_PROXY = env.str('OIDC_PROXY', default = None)
# This is a list of absolute url paths, regular expressions for url paths,
# or Django view names. This plus the mozilla-django-oidc urls are exempted
# from the session renewal by the SessionRefresh middleware.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_EXEMPT_URLS
OIDC_EXEMPT_URLS = env.list('OIDC_EXEMPT_URLS', default = [])
# Enables or disables automatic user creation during authentication
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_CREATE_USER
OIDC_CREATE_USER = env.bool('OIDC_CREATE_USER', default = True)
# Sets the length of the random string used for OpenID Connect
# state verification
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_STATE_SIZE
OIDC_STATE_SIZE = env.int('OIDC_STATE_SIZE', default = 32)
# Sets the length of the random string used for OpenID Connect
# nonce verification
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_NONCE_SIZE
OIDC_NONCE_SIZE = env.int('OIDC_NONCE_SIZE', default = 32)
# Sets the maximum number of State / Nonce combinations stored in the session.
# Multiple combinations are used when the user does multiple concurrent
# login sessions.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_MAX_STATES
OIDC_MAX_STATES = env.int('OIDC_MAX_STATES', default = 50)
# Sets the GET parameter that is being used to define the redirect URL after
# succesful authentication
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_REDIRECT_FIELD_NAME

#OIDC_REDIRECT_FIELD_NAME = env.str(
#    'OIDC_REDIRECT_FIELD_NAME', default = 'next')
# Allows you to substitute a custom class-based view to be used as
# OpenID Connect callback URL.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_CALLBACK_CLASS
#OIDC_CALLBACK_CLASS = env.str(
#    'OIDC_CALLBACK_CLASS',
#    default = 'mozilla_django_oidc.views.OIDCAuthenticationCallbackView')
# Allows you to substitute a custom class-based view to be used as OpenID
# Connect authenticate URL.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_AUTHENTICATE_CLASS
#OIDC_AUTHENTICATE_CLASS = env.str(
#    'OIDC_AUTHENTICATE_CLASS',
#    default = 'mozilla_django_oidc.views.OIDCAuthenticationRequestView')
# The OpenID Connect scopes to request during login.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_SCOPES
#OIDC_RP_SCOPES = env.str('OIDC_RP_SCOPES', default = 'openid email')
# Controls whether the OpenID Connect client stores the OIDC access_token in
# the user session.
# The session key used to store the data is oidc_access_token.
# By default we want to store as few credentials as possible so
# this feature defaults to False and it’s use is discouraged.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_STORE_ACCESS_TOKEN
#OIDC_STORE_ACCESS_TOKEN = env.bool('OIDC_STORE_ACCESS_TOKEN', default = False)
# Controls whether the OpenID Connect client stores the OIDC id_token in the
# user session. The session key used to store the data is oidc_id_token.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_STORE_ID_TOKEN
#OIDC_STORE_ID_TOKEN = env.bool('OIDC_STORE_ID_TOKEN', default = False)
# Additional parameters to include in the initial authorization request.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_AUTH_REQUEST_EXTRA_PARAMS
#OIDC_AUTH_REQUEST_EXTRA_PARAMS = env.list(
#    'OIDC_AUTH_REQUEST_EXTRA_PARAMS', default = [])
# Sets the algorithm the IdP uses to sign ID tokens.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_SIGN_ALGO
OIDC_RP_SIGN_ALGO = env.str('OIDC_RP_SIGN_ALGO', default = 'HS256')
# Sets the key the IdP uses to sign ID tokens in the case of an RSA sign
# algorithm. Should be the signing key in PEM or DER format.
# REQUIRED IF OIDC_OP_JWKS_ENDPOINT IS NOT SET
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_IDP_SIGN_KEY
#OIDC_RP_IDP_SIGN_KEY = env.bool('OIDC_RP_IDP_SIGN_KEY', default = None)
# Path to redirect to on successful login. If you don’t specify this,
# the default Django value will be used.
#LOGIN_REDIRECT_URL = env.str(
#    'LOGIN_REDIRECT_URL', default = BASE_URL)
# Path to redirect to on an unsuccessful login attempt.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#LOGIN_REDIRECT_URL_FAILURE
#LOGIN_REDIRECT_URL_FAILURE = env.str(
#    'LOGIN_REDIRECT_URL_FAILURE', default = '/')
# After the logout view has logged the user out, it redirects to this url path.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#LOGOUT_REDIRECT_URL
#LOGOUT_REDIRECT_URL = env.bool('LOGOUT_REDIRECT_URL', default = None)
# Function path that returns a URL to redirect the user to after
# auth.logout() is called.
# Changed in version 0.7.0: The function must now take a request parameter.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_OP_LOGOUT_URL_METHOD
#OIDC_OP_LOGOUT_URL_METHOD = env.str('OIDC_OP_LOGOUT_URL_METHOD', default = '')
# URL pattern name for OIDCAuthenticationCallbackView. Will be passed to
# reverse. The pattern can also include namespace in order to resolve
# included urls.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_AUTHENTICATION_CALLBACK_URL
#OIDC_AUTHENTICATION_CALLBACK_URL = env.str(
#    'OIDC_AUTHENTICATION_CALLBACK_URL',
#    default = 'oidc_authentication_callback')
# Controls whether the authentication backend is going to allow unsecured JWT
# tokens (tokens with header {"alg":"none"}). This needs to be set to True if
# OP is returning unsecured JWT tokens and RP wants to accept them.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_ALLOW_UNSECURED_JWT
OIDC_ALLOW_UNSECURED_JWT = env.bool(
    'OIDC_ALLOW_UNSECURED_JWT', default = False)
# Use HTTP Basic Authentication instead of sending the client secret in
# token request POST body.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_TOKEN_USE_BASIC_AUTH
#OIDC_TOKEN_USE_BASIC_AUTH = env.bool(
#    'OIDC_TOKEN_USE_BASIC_AUTH', default = False)
# Allow using GET method to logout user
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#ALLOW_LOGOUT_GET_METHOD
#ALLOW_LOGOUT_GET_METHOD = env.bool(
#    'ALLOW_LOGOUT_GET_METHOD', default = False)
# If you’ve created a custom Django OIDCAuthenticationBackend and added that
# to your AUTHENTICATION_BACKENDS, the DRF class should be smart enough to
# figure that out. Alternatively, you can manually set the OIDC backend to use:
# https://mozilla-django-oidc.readthedocs.io/en/stable/drf.html
OIDC_DRF_AUTH_BACKEND = 'scouts_auth.oidc.InuitsOIDCAuthenticationBackend'
# Depending on your OpenID Connect provider (OP) you might need to change the
# default signing algorithm from HS256 to RS256 by settings the
# OIDC_RP_SIGN_ALGO value accordingly.
# For RS256 algorithm to work, you need to set either the OP signing key or
# the OP JWKS Endpoint.
# The corresponding settings values are:
# OIDC_RP_IDP_SIGN_KEY = "<OP signing key in PEM or DER format>"
# OIDC_OP_JWKS_ENDPOINT = "<URL of the OIDC OP jwks endpoint>"
# If both specified, the key takes precedence.
# REQUIRED IF OIDC_RP_IDP_SIGN_KEY IS NOT SET
# https://mozilla-django-oidc.readthedocs.io/en/stable/installation.html
OIDC_OP_JWKS_ENDPOINT = correct_url(
    OIDC_OP_ISSUER, env.str('OIDC_OP_JWKS_ENDPOINT'))


logger.debug('OIDC_OP_ISSUER: ' + OIDC_OP_ISSUER)
logger.debug('OIDC_OP_JWKS_ENDPOINT: ' + OIDC_OP_JWKS_ENDPOINT)
logger.debug('OIDC_OP_TOKEN_ENDPOINT: ' + OIDC_OP_TOKEN_ENDPOINT)
logger.debug('OIDC_OP_USER_ENDPOINT: ' + OIDC_OP_USER_ENDPOINT)
logger.debug('OIDC_RP_CLIENT_ID: ' + OIDC_RP_CLIENT_ID)



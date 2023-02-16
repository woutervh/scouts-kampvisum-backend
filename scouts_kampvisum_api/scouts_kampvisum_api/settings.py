"""
Django settings for scouts_kampvisum_api project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# ############################################################################ #
#                                                                              #
# SENTRY                                                                       #
#                                                                              #
# ############################################################################ #
# https://docs.sentry.io/platforms/python/guides/django/
# ############################################################################ #
from environs import Env
import logging.config
import logging
import os
from scouts_auth.inuits.logging import InuitsLogger


# ############################################################################ #
#                                                                              #
# ENVIRONMENT                                                                  #
#                                                                              #
# ############################################################################ #
# Environment loading
env = Env()
env.read_env()

# ############################################################################ #
#                                                                              #
# DJANGO                                                                       #
#                                                                              #
# ############################################################################ #
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)
IS_ACCEPTANCE = env.bool("IS_ACCEPTANCE", default=False)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = env.str("BASE_URL", default="/")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# ############################################################################ #
#                                                                              #
# LOGGING                                                                      #
#                                                                              #
# ############################################################################ #
# https://stackoverflow.com/questions/53014435/why-is-logging-in-my-django-settings-py-ignored
LOGGING_CONFIG = None
LOGGING_LEVEL = env.str("LOGGING_LEVEL", "DEBUG")
LOGGING_LEVEL_ROOT = env.str("LOGGING_LEVEL_ROOT", "INFO")
LOGGING_LEVEL_DB = "INFO"
# LOGGING_LEVEL_DB = "DEBUG"
LOGGING_LEVEL_S3 = "INFO"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "incremental": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(levelname)-7s - %(name)-12s - %(message)s",
        },
        "simple": {
            "format": "%(levelname)-8s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
        # "file": {
        #     "class": "logging.FileHandler",
        #     "level": "DEBUG",
        #     "filename": "scouts-kampvisum.debug.log",
        # },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGGING_LEVEL_ROOT,
        # "level": LOGGING_LEVEL,
    },
    "loggers": {
        "mozilla_django_oidc": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "scouts_auth": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL_ROOT,
            "propagate": False,
        },
        "scouts_auth.groupadmin": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "rest_framework": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "drf-yasg2": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "botocore": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL_S3,
            "propagate": False,
        },
        "urllib3": {
            "handlers": None,
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL_DB,
            "propagate": False,
        },
    },
}


InuitsLogger.setup_logging(level=LOGGING_LEVEL, config=LOGGING)
logger: InuitsLogger = logging.getLogger(__name__)


def correct_url(issuer, url):
    if not url.startswith("http"):
        return issuer + url
    return url


# ############################################################################ #
#                                                                              #
# APPLICATIONS, MIDDLEWARE AND TEMPLATES                                       #
#                                                                              #
# ############################################################################ #
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "safedelete",
    "storages",
    "sqlmiddleware",
    "scouts_auth",
    "apps.utils",
    "apps.setup",
    "apps.participants",
    "apps.locations",
    "apps.visums",
    "apps.groups",
    "apps.camps",
    "apps.deadlines",
    "rest_framework",
    "django_filters",
    "drf_yasg2",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_cprofile_middleware.middleware.ProfilerMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ############################################################################ #
#                                                                              #
# BASIC APPLICATION                                                            #
#                                                                              #
# ############################################################################ #
ROOT_URLCONF = "scouts_kampvisum_api.urls"
WSGI_APPLICATION = "scouts_kampvisum_api.wsgi.application"


# ############################################################################ #
#                                                                              #
# PROFILER                                                                     #
#                                                                              #
# ############################################################################ #
DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False


# ############################################################################ #
#                                                                              #
# DATABASE                                                                     #
#                                                                              #
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases                #
#                                                                              #
# ############################################################################ #
DATABASES = {
    "default": {
        "ENGINE": env.str("DBENGINE"),
        "NAME": env.str("DBNAME"),
        "USER": env.str("DBUSER"),
        "PASSWORD": env.str("DBPASSWORD"),
        "HOST": env.str("DBHOST"),
        "PORT": env.str("DBPORT"),
    }
}
# DEFAULT PRIMARY KEY FIELD TYPE
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# ############################################################################ #
#                                                                              #
# BASIC SECURITY                                                               #
#                                                                              #
# ############################################################################ #
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
django_pw_validation = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": django_pw_validation + "UserAttributeSimilarityValidator",
    },
    {
        "NAME": django_pw_validation + "MinimumLengthValidator",
    },
    {
        "NAME": django_pw_validation + "CommonPasswordValidator",
    },
    {
        "NAME": django_pw_validation + "NumericPasswordValidator",
    },
]


# ############################################################################ #
#                                                                              #
# INTERNATIONALIZATION                                                         #
#                                                                              #
# https://docs.djangoproject.com/en/2.2/topics/i18n/                           #
#                                                                              #
# ############################################################################ #
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ############################################################################ #
#                                                                              #
# DJANGO REST FRAMEWORK                                                        #
#                                                                              #
# ############################################################################ #
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "scouts_auth.auth.oidc_auth.InuitsOIDCAuthentication",
        'rest_framework.authentication.SessionAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "scouts_kampvisum_api.pagination.PageNumberPagination",
    "EXCEPTION_HANDLER": "scouts_auth.inuits.exceptions.drf_exception_handler.drf_exception_handler",
}


# ############################################################################ #
#                                                                              #
# CORS                                                                         #
#                                                                              #
# ############################################################################ #
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")


# ############################################################################ #
#                                                                              #
# CHANGE HANDLERS                                                              #
#                                                                              #
# ############################################################################ #
CAMP_REGISTRATION_DEADLINE_NAME = "camp_registration"
DEADLINE_FLAG_CHANGED = "default_deadline_flag_changed"
CHECK_CHANGED = "default_check_changed"


# ############################################################################ #
#                                                                              #
# SCOUTS                                                                       #
#                                                                              #
# ############################################################################ #
USERNAME_FROM_ACCESS_TOKEN = env.bool("USERNAME_FROM_ACCESS_TOKEN", True)
SCOUTS_YEAR_START = env.str("SCOUTS_YEAR_START", "09-01")
SCOUTS_YEAR_END = env.str("SCOUTS_YEAR_END", "09-01")
INCLUDE_INACTIVE_FUNCTIONS_IN_PROFILE = env.bool(
    "INCLUDE_INACTIVE_FUNCTIONS_IN_PROFILE", False)
INCLUDE_ONLY_LEADER_FUNCTIONS_IN_PROFILE = env.bool(
    "INCLUDE_ONLY_LEADER_FUNCTIONS_IN_PROFILE", True)
INCLUDE_INACTIVE_MEMBERS_IN_SEARCH = env.bool(
    "INCLUDE_INACTIVE_MEMBERS_IN_SEARCH", False
)
BASE_AUTH_ROLES = env.list("BASE_AUTH_ROLES", [
                           "role_section_leader", "role_group_leader", "role_district_commissioner", "role_shire_president", "role_administrator"])
ACTIVITY_EPOCH = env.int("ACTIVITY_EPOCH", 3)
# Day after which a new camp registration is considered to be in the next camp year - FORMAT: MM-DD
CAMP_REGISTRATION_EPOCH = env.str("CAMP_REGISTRATION_EPOCH", "09-01")
# Deadline for the camp registration - FORMAT: MM-DD
CAMP_REGISTRATION_DEADLINE = env.str("CAMP_REGISTRATION_DEADLINE", "03-31")
# Day after which a mail should be sent if the camp responsible has changed - FORMAT: MM-DD
RESPONSIBILITY_EPOCH = env.str(
    "RESPONSIBILITY_EPOCH", CAMP_REGISTRATION_DEADLINE)
# Camp registration mails should be sent only once during this period (in hours)
CAMP_REGISTRATION_MAIL_DELTA = env.int("CAMP_REGISTRATION_MAIL_DELTA", 24)
ENFORCE_MEMBER_CHECKS = env.list(
    "ENFORCE_MEMBER_CHECKS",
    ["ParticipantMemberCheck", "ParticipantLeaderCheck",
        "ParticipantResponsibleCheck"],
)
PROFILE_REFRESH = env.int("PROFILE_REFRESH", 15)
PROFILE_REFRESH_GROUPS = env.int("PROFILE_REFRESH_GROUPS", 15)
PROFILE_REFRESH_FUNCTIONS = env.int("PROFILE_REFRESH_FUNCTIONS", 15)
# PROFILE_REFRESH = 0
# PROFILE_REFRESH_GROUPS = 0
# PROFILE_REFRESH_FUNCTIONS = 0
KNOWN_ADMIN_GROUPS = env.list("KNOWN_ADMIN_GROUPS")
KNOWN_TEST_GROUPS = env.list("KNOWN_TEST_GROUPS")
KNOWN_ROLES = env.list("KNOWN_ROLES")
LEADERSHIP_STATUS_IDENTIFIER = env.str(
    "LEADERSHIP_STATUS_IDENTIFIER", "Leiding")
GROUP_GENDER_IDENTIFIER_MALE = "S"
GROUP_GENDER_IDENTIFIER_FEMALE = "M"
CAMP_RESPONSIBLE_MIN_AGE = env.int("CAMP_RESPONSIBLE_MIN_AGE", 16)


# ############################################################################ #
#                                                                              #
# GROUPADMIN                                                                   #
#                                                                              #
# ############################################################################ #
GROUP_ADMIN_BASE_URL = env.str("GROUP_ADMIN_BASE_URL")
GROUP_ADMIN_ALLOWED_CALLS_ENDPOINT = GROUP_ADMIN_BASE_URL + "/"
GROUP_ADMIN_PROFILE_ENDPOINT = GROUP_ADMIN_BASE_URL + "/lid/profiel"
GROUP_ADMIN_MEMBER_SEARCH_ENDPOINT = GROUP_ADMIN_BASE_URL + "/zoeken"
GROUP_ADMIN_MEMBER_DETAIL_ENDPOINT = GROUP_ADMIN_BASE_URL + "/lid"
GROUP_ADMIN_MEMBER_LIST_ENDPOINT = GROUP_ADMIN_BASE_URL + "/ledenlijst"
GROUP_ADMIN_MEMBER_LIST_FILTERED_ENDPOINT = GROUP_ADMIN_BASE_URL + \
    "/ledenlijst/filter/stateless"
GROUP_ADMIN_GROUP_ENDPOINT = GROUP_ADMIN_BASE_URL + "/groep"
GROUP_ADMIN_FUNCTIONS_ENDPOINT = GROUP_ADMIN_BASE_URL + "/functie"


# ############################################################################ #
#                                                                              #
# PAGINATION                                                                   #
#                                                                              #
# ############################################################################ #
DEFAULT_PAGINATION_RESULTS = env.int("DEFAULT_PAGINATION_RESULTS", 10)
DEFAULT_PAGINATION_MAX_RESULTS = env.int(
    "DEFAULT_PAGINATION_MAX_RESULTS", 1000)
PARTICIPANT_PAGINATION_RESULTS = env.int("PARTICIPANT_PAGINATION_RESULTS", 20)
PARTICIPANT_PAGINATION_MAX_RESULTS = env.int(
    "PARTICIPANT_PAGINATION_MAX_RESULTS", 1000)


# ############################################################################ #
#                                                                              #
# STORAGE                                                                      #
#                                                                              #
# ############################################################################ #


# BASE FOLDERS
STATIC_URL = "static/"  # STATIC FILES (CSS, JavaScript, Images)
STATIC_ROOT = env.str("STATIC_ROOT")
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# FILE STORAGE
DEFAULT_FILE_STORAGE = env.str("DEFAULT_FILE_STORAGE")
# FILE_UPLOAD_ALLOWED_EXTENSIONS=jpg,jpeg,png,webp,odt,ods,odp,docx,pdf,pptx,xlsx
FILE_UPLOAD_ALLOWED_EXTENSIONS = env.list(
    "FILE_UPLOAD_ALLOWED_EXTENSIONS",
    [
        "jpg",
        "jpeg",
        "png",
        "webp",
        "odt",
        "ods",
        "odp",
        "docx",
        "doc",
        "pdf",
        "pptx",
        "xlsx",
    ],
)
# FILE_UPLOAD_MAX_SIZE=20971520 (20 MB)
FILE_UPLOAD_MAX_SIZE = env.int("FILE_UPLOAD_MAX_SIZE", 20971520)
OVERWRITE_EXISTING_FILE = env.bool("OVERWRITE_EXISTING_FILE")
FILE_UPLOAD_TMP_FOLDER = env.str("FILE_UPLOAD_TMP_FOLDER", "tmp_upload")


# S3
USE_S3_STORAGE = env.bool("USE_S3_STORAGE", False) == True
if USE_S3_STORAGE:
    AWS_ACCESS_KEY_ID = env.str("S3_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = env.str("S3_ACCESS_SECRET")
    AWS_STORAGE_BUCKET_NAME = env.str("S3_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = env.str("S3_ENDPOINT_URL")
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = OVERWRITE_EXISTING_FILE
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME", "eu-west-1")


# ############################################################################ #
#                                                                              #
# EMAIL                                                                        #
#                                                                              #
# ############################################################################ #


# EMAIL RESOURCES
RESOURCES_PATH = env.str("RESOURCES_PATH")
RESOURCES_MAIL_TEMPLATE_PATH = RESOURCES_PATH + \
    env.str("RESOURCES_MAIL_TEMPLATE_PATH")
RESOURCES_MAIL_TEMPLATE_START = RESOURCES_MAIL_TEMPLATE_PATH + env.str(
    "RESOURCES_MAIL_TEMPLATE_START"
)
RESOURCES_MAIL_TEMPLATE_END = RESOURCES_MAIL_TEMPLATE_PATH + env.str(
    "RESOURCES_MAIL_TEMPLATE_END"
)
RESOURCES_TEMPLATE_CAMP_REGISTRATION_BEFORE_DEADLINE = (
    RESOURCES_MAIL_TEMPLATE_PATH + "camp_registered_before_deadline.html"
)
RESOURCES_TEMPLATE_CAMP_REGISTRATION_AFTER_DEADLINE = (
    RESOURCES_MAIL_TEMPLATE_PATH + "camp_registered_after_deadline.html"
)
RESOURCES_TEMPLATE_CAMP_CHANGED_AFTER_DEADLINE = (
    RESOURCES_MAIL_TEMPLATE_PATH + "camp_changed_after_deadline.html"
)
RESOURCES_TEMPLATE_CAMP_RESPONSIBLE_CHANGED_AFTER_DEADLINE = (
    RESOURCES_MAIL_TEMPLATE_PATH + "camp_changed_after_deadline.html"
)

# EMAIL
EMAIL_DEBUG_RECIPIENT = env.str("EMAIL_DEBUG_RECIPIENT")
# We are going to use anymail which maps multiple providers like sendinblue with default django mailing code
# For more info see https://anymail.readthedocs.io/en/stable/esps/sendinblue/


def setup_mail():
    global USE_SENDINBLUE
    global EMAIL_BACKEND
    global ANYMAIL
    global EMAIL_TEMPLATE

    if USE_SENDINBLUE:
        API_KEY = env.str("SENDINBLUE_API_KEY")
        if DEBUG and not IS_ACCEPTANCE:
            API_KEY = env.str("SENDINBLUE_API_KEY_DEBUG", API_KEY)

        EMAIL_BACKEND = env.str("SENDINBLUE_BACKEND")
        ANYMAIL["SENDINBLUE_API_KEY"] = API_KEY
        ANYMAIL["SENDINBLUE_TEMPLATE_ID"] = env.str("SENDINBLUE_TEMPLATE_ID")
        EMAIL_TEMPLATE = ANYMAIL["SENDINBLUE_TEMPLATE_ID"]
    else:
        EMAIL_TEMPLATE = None


# DJANGO MAIL SETTINGS
EMAIL_BACKEND = env.str("EMAIL_BACKEND")
EMAIL_URL = env.str("EMAIL_URL")
EMAIL_SENDER = env.str("EMAIL_SENDER")
EMAIL_RECIPIENTS = env.str("EMAIL_RECIPIENTS", EMAIL_DEBUG_RECIPIENT)
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.str("EMAIL_PORT")
# SENDINBLUE EMAIL SETTINGS
USE_SENDINBLUE = env.bool("USE_SENDINBLUE", False)
SENDINBLUE_MAIL_TAGS = env.list("SENDINBLUE_MAIL_TAGS", ["Kampvisum"])
# SCOUTS KAMPVISUM EMAIL SETTINGS
# @TINUS moet toegevoegd worden in env of gewoon in settings ?
EMAIL_FROM = env.str("EMAIL_FROM", "kamp@scoutsengidsenvlaanderen.be")
EMAIL_REGISTRATION_BCC = env.str(
    "EMAIL_REGISTRATION_BCC", "bosaanvragen@scoutsengidsenvlaanderen.be"
)
EMAIL_REGISTRATION_SUBJECT = env.str(
    "EMAIL_REGISTRATION_SUBJECT", "Kampregistratie {}")
EMAIL_REGISTRATION_CHANGED_SUBJECT = env.str(
    "EMAIL_REGISTRATION_CHANGED_SUBJECT", "Je kampregistratie werd aangepast - {}"
)
EMAIL_RESPONSIBLE_CHANGED_SUBJECT = env.str(
    "EMAIL_RESPONSIBLE_CHANGED_SUBJECT",
    "Je kampregistratie werd aangepast - {}",
)
EMAIL_TEMPLATE = None
TMP_FOLDER = RESOURCES_PATH + "temp"
ANYMAIL = {}

setup_mail()

# ############################################################################ #
#                                                                              #
# REDIS CACHE                                                                  #
#                                                                              #
# ############################################################################ #
# REDIS_HOST = env.str("REDIS_HOST")
# REDIS_PORT = str(env.int("REDIS_PORT"))
# REDIS_KEY_PREFIX = env.str("REDIS_KEY_PREFIX")
# REDIS_PASSWORD = env.str("REDIS_PASSWORD")
# REDIS_USER_TTL = env.int("REDIS_USER_TTL", 10080)
# REDIS_PICKLE_VERSION = env.str("REDIS_PICKLE_VERSION", "-1")
# DJANGO_REDIS_IGNORE_EXCEPTIONS = env.bool("DJANGO_REDIS_IGNORE_EXCEPTIONS", True)
# DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = env.bool(
#     "DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS", True
# )
# REDIS_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": REDIS_URL,
#         "KEY_PREFIX": REDIS_KEY_PREFIX,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "PICKLE_VERSION": REDIS_PICKLE_VERSION,
#             "IGNORE_EXCEPTIONS": DJANGO_REDIS_IGNORE_EXCEPTIONS,
#         },
#         "KEY_PREFIX": "scouts",
#     }
# }
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"


# ############################################################################ #
#                                                                              #
# OIDC                                                                         #
#                                                                              #
# ############################################################################ #
AUTH_USER_MODEL = "scouts_auth.ScoutsUser"
AUTHORIZATION_ROLES_CONFIG_PACKAGE = "initial_data"
AUTHORIZATION_ROLES_CONFIG_YAML = "roles.yaml"
AUTHENTICATION_BACKENDS = [
    "scouts_auth.scouts.services.ScoutsOIDCAuthenticationBackend",
]

OIDC_OP_ISSUER = env.str("OIDC_OP_ISSUER")
# URL of your OpenID Connect provider authorization endpoint
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_OP_AUTHORIZATION_ENDPOINT
OIDC_OP_AUTHORIZATION_ENDPOINT = correct_url(
    OIDC_OP_ISSUER, env.str("OIDC_OP_AUTHORIZATION_ENDPOINT")
)
# URL of your OpenID Connect provider token endpoint
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_OP_TOKEN_ENDPOINT
OIDC_OP_TOKEN_ENDPOINT = correct_url(
    OIDC_OP_ISSUER, env.str("OIDC_OP_TOKEN_ENDPOINT"))
# URL of your OpenID Connect provider userinfo endpoint
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_OP_USER_ENDPOINT
OIDC_OP_USER_ENDPOINT = correct_url(
    OIDC_OP_ISSUER, env.str("OIDC_OP_USER_ENDPOINT"))
# OpenID Connect client ID provided by your OP
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_CLIENT_ID
OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID")
# OpenID Connect client secret provided by your OP
# REQUIRED
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_CLIENT_SECRET
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET")
# Controls whether the OpenID Connect client verifies the signature
# of the JWT tokens
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_VERIFY_JWT
OIDC_VERIFY_JWT = env.bool("OIDC_VERIFY_JWT", default=True)
# The jwt module can be configured to verify both the JWT and the JWT's signature.
# This setting is not part of mozilla_django_oidc
OIDC_VERIFY_JWT_SIGNATURE = env.bool(
    "OIDC_VERIFY_JWT_SIGNATURE", default=False)
# Controls whether the OpenID Connect client verifies the KID field
# of the JWT tokens
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_VERIFY_KID
OIDC_VERIFY_KID = env.bool("OIDC_VERIFY_KID", default=True)
# Controls whether the OpenID Connect client uses nonce verification
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_USE_NONCE
OIDC_USE_NONCE = env.bool("OIDC_USE_NONCE", default=True)
# Controls whether the OpenID Connect client verifies the SSL certificate of the OP responses
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_VERIFY_SSL
OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)
# Defines a timeout for all requests to the OpenID Connect provider
# (fetch JWS, retrieve JWT tokens, Userinfo Endpoint). The default is set to
# None which means the library will wait indefinitely. The time can be defined
# as seconds (integer). More information about possible configuration values,
# see Python requests:
# https://requests.readthedocs.io/en/master/user/quickstart/#timeouts
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_TIMEOUT
OIDC_TIMEOUT = env.int("OIDC_TIMEOUT", default=None)
# Defines a proxy for all requests to the OpenID Connect provider
# (fetch JWS, retrieve JWT tokens, Userinfo Endpoint). The default is set to
# None which means the library will not use a proxy and connect directly.
# For configuring a proxy check the Python requests documentation:
# https://requests.readthedocs.io/en/master/user/advanced/#proxies
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_PROXY
OIDC_PROXY = env.str("OIDC_PROXY", default=None)
# This is a list of absolute url paths, regular expressions for url paths,
# or Django view names. This plus the mozilla-django-oidc urls are exempted
# from the session renewal by the SessionRefresh middleware.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_EXEMPT_URLS
OIDC_EXEMPT_URLS = env.list("OIDC_EXEMPT_URLS", default=[])
# Enables or disables automatic user creation during authentication
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_CREATE_USER
OIDC_CREATE_USER = env.bool("OIDC_CREATE_USER", default=True)
# Sets the length of the random string used for OpenID Connect
# state verification
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_STATE_SIZE
OIDC_STATE_SIZE = env.int("OIDC_STATE_SIZE", default=32)
# Sets the length of the random string used for OpenID Connect
# nonce verification
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_NONCE_SIZE
OIDC_NONCE_SIZE = env.int("OIDC_NONCE_SIZE", default=32)
# Sets the maximum number of State / Nonce combinations stored in the session.
# Multiple combinations are used when the user does multiple concurrent
# login sessions.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_MAX_STATES
OIDC_MAX_STATES = env.int("OIDC_MAX_STATES", default=50)
# Sets the GET parameter that is being used to define the redirect URL after
# succesful authentication
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_REDIRECT_FIELD_NAME
# OIDC_REDIRECT_FIELD_NAME = env.str(
#    'OIDC_REDIRECT_FIELD_NAME', default = 'next')
# Allows you to substitute a custom class-based view to be used as
# OpenID Connect callback URL.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_CALLBACK_CLASS
# OIDC_CALLBACK_CLASS = env.str(
#    'OIDC_CALLBACK_CLASS',
#    default = 'mozilla_django_oidc.views.OIDCAuthenticationCallbackView')
# Allows you to substitute a custom class-based view to be used as OpenID
# Connect authenticate URL.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_AUTHENTICATE_CLASS
# OIDC_AUTHENTICATE_CLASS = env.str(
#    'OIDC_AUTHENTICATE_CLASS',
#    default = 'mozilla_django_oidc.views.OIDCAuthenticationRequestView')
# The OpenID Connect scopes to request during login.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_SCOPES
# OIDC_RP_SCOPES = env.str('OIDC_RP_SCOPES', default = 'openid email')
# Controls whether the OpenID Connect client stores the OIDC access_token in
# the user session.
# The session key used to store the data is oidc_access_token.
# By default we want to store as few credentials as possible so
# this feature defaults to False and it’s use is discouraged.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_STORE_ACCESS_TOKEN
# OIDC_STORE_ACCESS_TOKEN = env.bool('OIDC_STORE_ACCESS_TOKEN', default = False)
# Controls whether the OpenID Connect client stores the OIDC id_token in the
# user session. The session key used to store the data is oidc_id_token.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_STORE_ID_TOKEN
# OIDC_STORE_ID_TOKEN = env.bool('OIDC_STORE_ID_TOKEN', default = False)
# Additional parameters to include in the initial authorization request.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_AUTH_REQUEST_EXTRA_PARAMS
# OIDC_AUTH_REQUEST_EXTRA_PARAMS = env.list(
#    'OIDC_AUTH_REQUEST_EXTRA_PARAMS', default = [])
# Sets the algorithm the IdP uses to sign ID tokens.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_SIGN_ALGO
OIDC_RP_SIGN_ALGO = env.str("OIDC_RP_SIGN_ALGO", default="RS256")
# Sets the key the IdP uses to sign ID tokens in the case of an RSA sign
# algorithm. Should be the signing key in PEM or DER format.
# REQUIRED IF OIDC_OP_JWKS_ENDPOINT IS NOT SET
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_RP_IDP_SIGN_KEY
# OIDC_RP_IDP_SIGN_KEY = env.bool('OIDC_RP_IDP_SIGN_KEY', default = None)
# Path to redirect to on successful login. If you don’t specify this,
# the default Django value will be used.scouts_authn/stable/settings.html#LOGOUT_REDIRECT_URL
# LOGOUT_REDIRECT_URL = env.bool('LOGOUT_REDIRECT_URL', default = None)
# Function path that returns a URL to redirect the user to after
# auth.logout() is called.
# Changed in version 0.7.0: The function must now take a request parameter.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_OP_LOGOUT_URL_METHOD
# OIDC_OP_LOGOUT_URL_METHOD = env.str('OIDC_OP_LOGOUT_URL_METHOD', default = '')
# URL pattern name for OIDCAuthenticationCallbackView. Will be passed to
# reverse. The pattern can also include namespace in order to resolve
# included urls.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_AUTHENTICATION_CALLBACK_URL
# OIDC_AUTHENTICATION_CALLBACK_URL = env.str(
#    'OIDC_AUTHENTICATION_CALLBACK_URL',
#    default = 'oidc_authentication_callback')
# Controls whether the authentication backend is going to allow unsecured JWT
# tokens (tokens with header {"alg":"none"}). This needs to be set to True if
# OP is returning unsecured JWT tokens and RP wants to accept them.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_ALLOW_UNSECURED_JWT
OIDC_ALLOW_UNSECURED_JWT = env.bool("OIDC_ALLOW_UNSECURED_JWT", default=False)
# Use HTTP Basic Authentication instead of sending the client secret in
# token request POST body.
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#OIDC_TOKEN_USE_BASIC_AUTH
# OIDC_TOKEN_USE_BASIC_AUTH = env.bool(
#    'OIDC_TOKEN_USE_BASIC_AUTH', default = False)
# Allow using GET method to logout user
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html#ALLOW_LOGOUT_GET_METHOD
# ALLOW_LOGOUT_GET_METHOD = env.bool(
#    'ALLOW_LOGOUT_GET_METHOD', default = False)
# If you’ve created a custom Django OIDCAuthenticationBackend and added that
# to your AUTHENTICATION_BACKENDS, the DRF class should be smart enough to
# figure that out. Alternatively, you can manually set the OIDC backend to use:
# https://mozilla-django-oidc.readthedocs.io/en/stable/drf.html
OIDC_DRF_AUTH_BACKEND = "scouts_auth.scouts.services.ScoutsOIDCAuthenticationBackend"
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
    OIDC_OP_ISSUER, env.str("OIDC_OP_JWKS_ENDPOINT"))

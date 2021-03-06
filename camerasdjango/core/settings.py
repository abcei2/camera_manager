""" TUCANO AR """

import os
import sys

from django.utils.translation import ugettext_lazy as _

from core.system import (
    PLACEHOLDER_FOR_SECRET,
    load_env_settings,
)

DJANGO_ENV = os.getenv('DJANGO_ENV', 'DEV').upper()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.abspath(os.path.join(REPO_DIR, 'data'))
MEDIA_DIR = os.path.abspath(os.path.join(DATA_DIR, 'media'))
ENV_DIR = os.path.join(REPO_DIR, 'env')
ENV_SECRETS_FILE = os.path.join(ENV_DIR, 'secrets.env')

FACES_DIR = os.path.abspath(os.path.join(MEDIA_DIR, 'faces'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = PLACEHOLDER_FOR_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
IS_RUNSERVER = 'runserver' in sys.argv
IS_TEST = 'test' in sys.argv
IS_MIGRATE = 'migrate' in sys.argv
ENABLE_DEBUG_TOOLBAR = False

ALLOWED_HOSTS = ["*"]
USE_X_FORWARDED_HOST = True
JSON_DIR = os.path.join(BASE_DIR, 'json')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILES_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')


# Don't change values here, only set these values in your env/secrets.env file
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DB = PLACEHOLDER_FOR_SECRET
POSTGRES_USER = PLACEHOLDER_FOR_SECRET
POSTGRES_PASSWORD = PLACEHOLDER_FOR_SECRET


###############################################################################
# App settings
###############################################################################

# parking
MAP_API = PLACEHOLDER_FOR_SECRET
FETCH_ZONES_INTERVAL = 20000
MAX_ZONE_REQUESTS = 7           # Max number of requests on an opened page
CAMERA_RADIUS = 500             # Radius for looking near cameras [m]
CAR_CLS_NAMES = ['person']
CAR_SCORE = 0.8
PEDESTRIAN_CLS_NAMES = ['person']
PEDESTRIAN_SCORE = 0.8
ENABLE_DETECTOR = True
ENABLE_FALSE_DETECTOR = False


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Load Settings Overrides from Environment Config Files
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# settings defined above in this file (settings.py)
SETTINGS_DEFAULTS = load_env_settings(env=globals())

# settings set via env/secrets.env
ENV_SECRETS = load_env_settings(
    dotenv_path=ENV_SECRETS_FILE, defaults=globals())
globals().update(ENV_SECRETS)

# settings set via environemtn variables
ENV_OVERRIDES = load_env_settings(env=dict(os.environ), defaults=globals())
globals().update(ENV_OVERRIDES)
SETTINGS_SOURCES = {
    'settings.py': SETTINGS_DEFAULTS,
    ENV_SECRETS_FILE: ENV_SECRETS,
    'os.environ': ENV_OVERRIDES,
}
# To track down where a specific setting is being imported from:
# print('Setting sources: \n{SETTINGS_SOURCES}')
# print(config.system.get_setting_source(SETTING_NAME))


###############################################################################
# Application definition
###############################################################################

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',

    'django_extensions',
    'crispy_forms',
    'chartjs',

    'core',
    'cameras',
    'face_recognition',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_DIRS = [STATICFILES_DIR]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, JSON_DIR],
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

AUTH_USER_MODEL = 'cameras.User'
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

###############################################################################
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
###############################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'NAME': POSTGRES_DB,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (prod subpath)
if DJANGO_ENV == 'PROD':
    FORCE_SCRIPT_NAME = '/cameras/'
    STATIC_URL = '/cameras/static/'
    MEDIA_URL = '/cameras/media/'
    LOGIN_REDIRECT_URL = '/cameras/cameras/manage_cameras/'
    LOGOUT_REDIRECT_URL = '/cameras/login/'

else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    LOGIN_REDIRECT_URL = '/cameras/manage_cameras/'
    LOGOUT_REDIRECT_URL = '/login/'


# Debug toolbar
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS = [
        'debug_toolbar',
    ] + INSTALLED_APPS
    MIDDLEWARE = MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INTERNAL_IPS = ['127.0.0.1']

"""
Django settings for hire_gurkha_backend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
import environ
env = environ.Env(
    DEBUG=(bool, False),
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'backend',
    'recruiter',
    'job_seeker',
    'blog',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail_modeladmin',
    'wagtail',
     'wagtail.api.v2',
    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "debug_toolbar",
    'corsheaders',
    'rest_framework',
    'django_rest_passwordreset',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]
INTERNAL_IPS = [
    
    "127.0.0.1",
    
]
CORS_ORIGIN_ALLOW_ALL  = True

ROOT_URLCONF = 'hire_gurkha_backend.urls'

WAGTAIL_SITE_NAME = 'Hire Gurkha'

WAGTAILADMIN_BASE_URL = 'http://127.0.0.1:8000'

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

WSGI_APPLICATION = 'hire_gurkha_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'hire_gurkha_db', # database name
            'HOST':'localhost', # database servername
            'USER':os.environ.get("DB_USER"), 
            'PASSWORD':os.environ.get("DB_PASSWORD"),
            'PORT':'3306',
        }
        
    }

DOMAIN_NAME = 'api.hiregurkha.com'
REST_FRAMEWORK = {
   
    'DEFAULT_AUTHENTICATION_CLASSES': (
       
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
   
}

SIMPLE_JWT = {
 
  "TOKEN_OBTAIN_SERIALIZER": "recruiter.serializers.MyTokenObtainPairSerializer",
   "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
 
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "backend.CustomUser"

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


#Email Confguration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
# STATICFILES_DIRS = [
#     os.path.join(PROJECT_DIR, "static"),
# ]

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"


STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 5


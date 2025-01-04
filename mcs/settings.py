from pathlib import Path
# from unipath import Path
from decouple import config, Csv
# from unipath import Path
from dj_database_url import parse as db_url

import os
# from os import getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY

# SECURITY WARNING: keep the secret key used in production secret!
# Python Decouple Settings
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# In Production stage IS_DEVLOPMENT is set to Flase So DEBUG = False


# DEBUG Settings
# Django Default Settings
# DEBUG = True
# Python Decouple Settings
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS Settings
# Django Default Settings
# ALLOWED_HOSTS = ["*",]
# Python Decouple Settings
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())


# Application definition

CRISPY_TEMPLATE_PACK = "bootstrap4"  # Slick Reporting Apps

INSTALLED_APPS = [
    'backend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',  # For allowing Cross-Origin Requests
    "slick_reporting",  # Slick Reporting Apps
    "crispy_forms",  # Slick Reporting Apps
    "crispy_bootstrap4",  # Slick Reporting Apps
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcs.urls'

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

WSGI_APPLICATION = 'mcs.wsgi.application'


# Database

# Local MySQL Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mcsdb',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '3306'
#     }
# }

# Django Default Settings
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db1.sqlite3',
#     }
# }


# Python Decouple Settings
DATABASES = {
    'default': config(
        'DATABASE_URL',
        default=BASE_DIR / 'db.sqlite3',
        cast=db_url
    )
}
# Python Decouple Default Settings
# DATABASES = {
#     'default': config(
#         'DATABASE_URL',
#         default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
#         cast=db_url
#     )
# }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# To change default user model
# AUTH_USER_MODEL = 'your_app_name.CustomUser'
AUTH_USER_MODEL = 'backend.Employee'


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC' # Default TimeZone

TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Use manage.py collectstatic to collect all static files to this folder
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

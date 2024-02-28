"""
Django settings for ddaniela_handmade project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url


if os.path.isfile('env.py'):
    import env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f+*9f8_b(j^%2!q9gk2s-xsy9^72t*=#a3w(7cn0j8o9yez*i*'
# CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',
                 '8000-bogdan-branzaniuc-daniel-lclgw5yfjk.us2.codeanyapp.com',
                 'daniela-handmade-8a9762fab1c1.herokuapp.com']

# Application definition
SITE_ID = 2

SOCIALACCOUNT_EMAIL_REQUIRED = True

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_unicorn',
    'home',
    'profiles',
    'products',
    'bag',
    'checkout',
    'django_countries',
    'colorfield',
    'cloudinary_storage',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap4',
    'webcolors',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}

SOCIALACCOUNT_STORE_TOKENS = True

CSRF_TRUSTED_ORIGINS = [
    'https://daniela-handmade-8a9762fab1c1.herokuapp.com',
    'https://8000-bogdan-branzaniuc-daniel-lclgw5yfjk.us2.codeanyapp.com']

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'daniela_handmade.urls'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'home'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
            os.path.join(BASE_DIR, 'templates', 'errors'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bag.sessionbag.bag_contents'
            ],
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]


WSGI_APPLICATION = 'daniela_handmade.wsgi.application'


# Database
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# cloudinary.config(
#     cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
#     api_key=os.getenv('CLOUDINARY_API_KEY'),
#     api_secret=os.getenv('CLOUDINARY_API_SECRET')
# )

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STRIPE_CURRENCY = 'eur'
# STRIPE_PUBLIC_KEY = 'pk_test_51OL3NULW8TXmjJXuYR63Zpefw9PpQCFfwhZkMhsDMKBlaXMT421bRotLJ4Zqs63mjnAXArmTYz8aAP7hB5zsjNbA00D8EB9DcB'
# STRIPE_SECRET_KEY = 'sk_test_51OL3NULW8TXmjJXuTD4QizPe7nHXyvvGun6zV3FnPHM8RsCtZ378hfarx1lHyCUwsdeS71IaAyUpm6bts8kfYZu700sSal4MEU'
# STRIPE_WH_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'alimoeed15@gmail.com'
EMAIL_HOST_PASSWORD = 'chph huap srra mlon'

FREE_DELIVERY_THRESHOLD = 25
STANDARD_DELIVERY_PERCENTAGE = 10
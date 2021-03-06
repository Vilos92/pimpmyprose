"""
Django settings for pimpmyprose project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vp)5*$&ro6-0+j5nvpgsubu9%3cvhvyw8z$-2g9@24cse+h7=4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = [ os.path.join( BASE_DIR, 'templates' ) ]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

	# App for searching
	'haystack',

    # App for Django Rest Framework
    'rest_framework',

	# pimpMyProse app
	'prose',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pimpmyprose.urls'

WSGI_APPLICATION = 'pimpmyprose.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pimpmyprose',
		'USER': 'linschei',
		'PASSWORD': 'LaMarcusSup4',
		'HOST': '127.0.0.1',
		'PORT': '5432',
    }
}

# Connections so Haystack can search models
HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE' : 'haystack.backends.whoosh_backend.WhooshEngine',
		'PATH' : os.path.join( os.path.dirname( __file__ ), 'whoosh_index' ),
	},
}

# Allow haystack to update in real time
# May need to change this to reduce load in production
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Use a reverse here if possible
LOGIN_URL = 'prose:login'

TIME_ZONE = 'US/Pacific'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(
        os.path.dirname(__file__),
        'static',
    ),
)

# Default settings for the rest_framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES' : ( 'rest_framework.permissions.IsAuthenticatedOrReadOnly', ),
    'PAGE_SIZE' : 10
}

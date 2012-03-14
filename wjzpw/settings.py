from os import path
import sys, os
# Django settings for wjzpw project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.getcwd()
WEBVERSE_DIR = '/wjzpw/webverse'

ADMINS = (
    # ('Winston Ng', 'winston@xplusz.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'wjzpw',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',          
        'PORT': '5432',              
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'
DEFAULT_CHARSET='utf-8'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_DIR + WEBVERSE_DIR

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=n9qnu(k1qr*m%z=24r2n*0_es&ea==qqpnv&edl=riykcb4)^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'wjzpw.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # IMPORTANT - this path only works for "foreman start" and not the typical "runserver" command.
    PROJECT_DIR + "/wjzpw/webverse/views"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'gunicorn',
    'webverse',
    'jsonrpc',
)

AUTH_PROFILE_MODULE = 'webverse.UserProfile'

AUTHENTICATION_BACKENDS = (
    'webverse.controllers.backend.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

#######################################################################################################################
# APPLICATION LEVEL SETTINGS
# Leave it here for now but might want to specify in DB down the road for configuration.
#######################################################################################################################

# Suggested exercise time required per day. In minutes.
DAILY_EXERCISE_TIME = 60

#######################################################################################################################
# SESSION EXPIRATION SETTINGS
#######################################################################################################################
LOGIN_URL  = "/"

#Limit session expire time to 20 minutes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 1200

#######################################################################################################################
# MAIL SERVER SETTINGS
#######################################################################################################################
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.126.com'
EMAIL_HOST_USER = 'digiod_no_reply@126.com'
EMAIL_HOST_PASSWORD = 'Mercury'
EMAIL_PORT = 25
EMAIL_FROM_USER = 'digiod_no_reply@126.com'

PROJECT_ROOT = path.abspath(path.dirname(__file__))
sys.path.append(path.join(PROJECT_ROOT, 'config'))


ENVIRONMENT='%ENVIRONMENT%'

# Set the ENVIRONMENT to dev if cookie not set which means it's local dev.
if 'ENVIRONMENT' in ENVIRONMENT:
    ENVIRONMENT = 'dev'

try:
    env = __import__('settings_'+ENVIRONMENT)
except:
    env = __import__('settings_dev')

for value in dir(env):
    if not value.startswith('__'):
        globals()[value] = getattr(env, value)

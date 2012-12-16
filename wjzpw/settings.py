# coding: utf-8
from os import path
import sys, os
import dj_database_url
# Django settings for wjzpw project.

# Register database schemes in URLs.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.getcwd()
WEBVERSE_DIR = '/wjzpw/web/'

ADMINS = (
     ('Jiang Chen', 'xxshutong@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgres://postgres:postgres@localhost/wjzpw')}

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
    'django.contrib.messages.context_processors.messages'
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
    PROJECT_DIR + "/wjzpw/web/views"
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
    'wjzpw.web',
    'jsonrpc',
    'tinymce'
)

AUTH_PROFILE_MODULE = 'web.UserProfile'

AUTHENTICATION_BACKENDS = (
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
# WJZPW APPLICATION SETTINGS
#######################################################################################################################
ANNOUNCEMENT_LIMIT_SIZE = 5
DASHBOARD_VIP_SIZE = 20
DASHBOARD_JOB_SIZE = 20
DASHBOARD_PERSON_SIZE = 20
SEARCH_JOB_SIZE = 10
SEARCH_RESUME_SIZE = 10
# 上传简历头像大小限制 byte
AVATAR_SIZE_LIMIT = 2*1024*1024

#######################################################################################################################
# SESSION EXPIRATION SETTINGS
#######################################################################################################################
LOGIN_URL  = "/login/"

#Limit session expire time to 20 minutes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 1200


#######################################################################################################################
# Verification code
#######################################################################################################################
NAME = u'captcha'
LETTERS = u'1234567890' #ABCDEFGHIJKLMNOPQRSTUVWXYZ'
COLOURS = (
    (203,61,27),
    (39,151,58),
    (0,139,120),
    (0,151,220),
    (1,53,146),
    (129,30,104),
    (183,1,111),
    (230,0,58),
    (0,0,0),
    )
FONTS = (
    u'ariblk.ttf',
    u'comic.ttf',
    u'georgia.ttf',
    u'impact.ttf',
    u'tahomabd.ttf',
    )
FONT_SIZE = 12
LENGTH = 5


#######################################################################################################################
# MAIL SERVER SETTINGS
#######################################################################################################################
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USERNAME', 'ipswitcher001@gmail.com')
#EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'wjzpwwjzpw')
#EMAIL_FROM_USER = u'吴江-招聘网wj-zpw.com'
#ADMIN_EMAIL = 'xxshutong@gmail.com'
# Email expiry time (days)
EMAIL_EXPIRE_TIME = 7

#######################################################################################################################
# TINYMCE PLUGIN CONFIG
#######################################################################################################################
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
    'theme': "advanced",
    'cleanup_on_startup': True,

    'theme_advanced_buttons1' : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
    'theme_advanced_buttons2' : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
    'theme_advanced_buttons3' : "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
    'theme_advanced_buttons4' : "insertlayer,moveforward,movebackward,absolute,|,styleprops,spellchecker,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,template,blockquote,pagebreak,|,insertfile,insertimage",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_statusbar_location' : "bottom",
    'theme_advanced_resizing' : True,
    }

#######################################################################################################################
# USER PROFILE
#######################################################################################################################
AUTH_PROFILE_MODULE = 'web.UserProfile'

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

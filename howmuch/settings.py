import os, sys
import dj_database_url

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

gettext_noop = lambda s: s


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Juan Carlos Cayetano', 'jc@brainn.co'),
)

AUTH_PROFILE_MODULE = 'profile.Profile'

MANAGERS = ADMINS

#import dj_database_url   # use this to setup in localsettings.
DATABASES = {'default':
                   dj_database_url.config(
                  default='postgres://kayethano:90ldenb0y@localhost:5432/howmuch')
        }
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Mexico/General'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-MX'

LANGUAGES = (

('es-mx', gettext_noop('Mexican Spanish')),

)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

#Site Root
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#AMAZON
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJBJPT42ROYJRYKFA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'howmuch'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#AMAZON

#FILES

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

#FILES

#REGISTRATION
ACCOUNT_ACTIVATION_DAYS = 7
#REGISTRATION

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1afjnj#t5sf=d3n@1v#0)a=y$j-3818co1j5bm988!gqdhzg_w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'django_facebook.context_processors.facebook',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_facebook.auth_backends.FacebookBackend',
)

ROOT_URLCONF = 'howmuch.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'howmuch.wsgi.application'

TEMPLATE_DIRS = ( os.path.join(SITE_ROOT, 'templates'),)

INSTALLED_APPS = (

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.formtools',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    #'endless_pagination',
    'gunicorn',
    'storages',
    
    'howmuch.about',
    'howmuch.account',
    'howmuch.article',
    'howmuch.backend',
    'howmuch.category',
    'howmuch.comments',
    'howmuch.config',
    'howmuch.invoice',
    'howmuch.messages',
    'howmuch.notifications',
    'howmuch.pays',
    'howmuch.pictures',
    'howmuch.prestige',
    'howmuch.problems',
    'howmuch.profile',
    'howmuch.search',
    'howmuch.tags',

    'registration',
    'paypal.standard.ipn',
    'django_facebook',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BROKER_BACKEND = 'django'

LOGIN_REDIRECT_URL = '/'


#EMAIL
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'app11900803@heroku.com'
EMAIL_HOST_PASSWORD = 'gff4vexq'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@comprateca.com'


#Facebook Settings
FACEBOOK_APP_ID = '151714724990012'
FACEBOOK_APP_SECRET = '96c602d1701ce53c3241652cdec8d6fd' 

#Comission 
COMMISSION = .05

#Points for Action
POINTS_FOR_PUBLISH = 5
POINTS_FOR_OFFER = 5
POINTS_FOR_SELECT = 5
POINTS_FOR_ASSIGNMNET = 10
POINTS_FOR_CRITIQUE = 5
POINTS_FOR_POSITIVE_CRITIQUE = 10
POINTS_FOR_NEGATIVE_CRITIQUE = 15


#Plazo en dias para pagar la factura
DAYS_LIMIT_INVOICE = 7

PRESTIGE_TYPES = {
    'PRESTIGE1' : {
        'NAME' : 'SIRIUS',
        'INTERVAL' : [0,100],
        'LIMIT' : 200
    },
    'PRESTIGE2' : {
        'NAME' : 'ANTARES',
        'INTERVAL' : [101,500],
        'LIMIT' : 1000
    },
    'PRESTIGE3' : {
        'NAME' : 'MU CEPHEI',
        'INTERVAL' : [501,2000],
        'LIMIT' : 2000
    },
    'PRESTIGE4' : {
        'NAME' : 'CANIS MAJORIS',
        'INTERVAL' : [2001,],
        'LIMIT' : 5000
    }
}

#SITE OFFICIAL URL
URL_OFFICIAL_SITE = 'http://www.comprateca.com'

#CHANGE PASSWORD REDIRECT 
CHANGE_CONFIG_REDIRECT = '/config/notifications/?change_config=True'

#PAYPAL EMAIL
PAYPAL_RECEIVER_EMAIL = "paypal@brainn.co"

SEARCHIFY_INDEX = 'idx'


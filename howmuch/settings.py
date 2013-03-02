import os, sys
import dj_database_url

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

gettext_noop = lambda s: s


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Juan Carlos Cayetano', 'kayethano@gmail.com'),
    ('Joel Rivera', 'rivera@joel.mx'),
)

AUTH_PROFILE_MODULE = 'profile.profile'

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
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
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

    'endless_pagination',
    'gunicorn',
    'storages',
    'django_facebook',
    
    'howmuch.account',
    'howmuch.article',
    'howmuch.backend',
    'howmuch.comments',
    'howmuch.config',
    'howmuch.invoice',
    'howmuch.messages',
    'howmuch.notifications',
    'howmuch.pictures',
    'howmuch.prestige',
    'howmuch.problems',
    'howmuch.profile',
    'howmuch.search',


    'registration',
    'tagging',



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
DEFAULT_FROM_EMAIL = 'noreply@houmuch.com'


#Cuantoo.com Facebook Settings
FACEBOOK_APP_ID = '429046753838184'
FACEBOOK_APP_SECRET = 'f25118e2c2043d335d5aebecded78976' 
#FACEBOOK_REGISTRATION_BACKEND = 'registration.backends.default.DefaultBackend'

#Comission 
COMMISSION = .05

#Points for Action
POINTS_FOR_PUBLISH = 5
POINTS_FOR_OFFER = 5
POINTS_FOR_SELECT = 5
POINTS_FOR_ASSIGNMNET = 10
POINTS_FOR_CRITIQUE = 5


import os
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF = 'poemradio.urls'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1','.poemrad.io']


INSTALLED_APPS = [
    'tagging',
    'poem.apps.PoemConfig',
    'django.contrib.sites',
    'anymail',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #todo: allow facebook and google authentication
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    'poemUser.apps.PoemuserConfig',
    'tags.apps.TagsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

FORCE_LOWERCASE_TAGS = True

#Site ID in database is pk=3, "poemrad.io"
SITE_ID = 3

#Require email, username for signup and allow either for sign in
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED =True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
#Make usernames case insensitive
ACCOUNT_PRESERVE_USERNAME_CASING = False
#Custom signup form, allows PoemUser instantiation and collects first/last name.
ACCOUNT_SIGNUP_FORM_CLASS = 'poemUser.forms.SignupForm'

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = "/"




MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, "..", 'templates').replace('\\','/'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'poemradio.wsgi.application'

#default database setting

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#reset db based on env

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

#TODO: HTTPS configuration
# CSRF_COOKIE_SECURE = True

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Static files

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# POSTMARK_SENDER      = 'sender@poemrad.io'
POSTMARK_TEST_MODE   = False
POSTMARK_TRACK_OPENS = True
#Email
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

# EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"  
DEFAULT_FROM_EMAIL = "Little PoemRad.io Robot <lilrobot@poemrad.io>"  

#Load env key only if no local settings
try:
    from .local_settings import *
except ImportError as e:
    # ANYMAIL = {
    #     "MAILGUN_API_KEY": os.environ['MAILGUN_API_KEY'],
    #     "MAILGUN_SENDER_DOMAIN": 'mg.poemrad.io',  
    # }
    POSTMARK_API_KEY     = os.environ['POSTMARK_API_TOKEN']
    


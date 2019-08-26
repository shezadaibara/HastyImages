import os
from .configs import MYSQL, RABBIT_MQ, S3_CONFIG

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '70)#eh-_l%gcx(lftwkrg$2@poqtn20s4(g@!z%y8(ql%y^@g2i-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'invitation.apps.InvitationConfig',
    'gallery.apps.GalleryConfig',
    'django_celery_results'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL['db'],
        'USER': MYSQL['username'],
        'PASSWORD': MYSQL['password'],
        'HOST': MYSQL['host'],
        'PORT': MYSQL['port'],
        'TEST': {
            'NAME': MYSQL['test_db'],
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_WHITELIST = (
    'localhost:9001', '127.0.0.1:9001', 'minio1:9001'
)

Pagination_class = 'rest_framework.pagination.PageNumberPagination'
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': Pagination_class,
    'PAGE_SIZE': 20
}

# A Token by default expires in 10days
import datetime
DEFAULT_TOKEN_EXPIRE_TIMESPAN = datetime.timedelta(days=7)

STATIC_URL = '/static/'
STATIC_ROOT = './static_files/'


CELERY_RESULT_BACKEND = 'django-db'

RABBIT_HOSTNAME = os.environ.get('RABBIT_PORT_5672_TCP', RABBIT_MQ['host'])

if RABBIT_HOSTNAME.startswith('tcp://'):
    RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

CELERY_BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
    user=os.environ.get('RABBIT_ENV_USER', RABBIT_MQ['user']),
    password=os.environ.get('RABBIT_ENV_RABBITMQ_PASS', RABBIT_MQ['password']),
    hostname=RABBIT_HOSTNAME,
    vhost=os.environ.get('RABBIT_ENV_VHOST', RABBIT_MQ['vhost']))
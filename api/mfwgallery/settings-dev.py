""" 
Django settings for ankkabot project. For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see                                                                                                                                                                 
https://docs.djangoproject.com/en/1.6/ref/settings/                                                                                                                                                                 
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)                                                                                                                                             
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = '/home/ankkamies/Projects/mfwgallery-web/public/media/'
STATIC_ROOT = '/home/ankkamies/Projects/mfwgallery-web/public/static/'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

REST_FRAMEWORK = {

        'DEFAULT_AUTHENTICATION_CLASSES': ( 
            'mfwgallery.authentication.QuietBasicAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
}
"""
        'DEFAULT_RENDERER_CLASSES': ( 
            'rest_framework.renderers.JSONRenderer', 
        )
}
"""

# Quick-start development settings - unsuitable for production                                                                                                                                                      
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/                                                                                                                                             

# SECURITY WARNING: keep the secret key used in production secret!                                                                                                                                                  
SECRET_KEY = '2^+m2aytjfb27sesi+w1g^o&o_-312=3jtq+(z&-1$wml&1w*q'

# SECURITY WARNING: don't run with debug turned on in production!                                                                                                                                                   
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition                                                                                                                                                                                            

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_nested',
    'posts'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_WHITELIST = (
    'localhost:9001'
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'accept-encoding',
    'origin',
    'authorization',
    'X-CSRFToken'
)

ROOT_URLCONF = 'mfwgallery.urls'

WSGI_APPLICATION = 'mfwgallery.wsgi.application'

# Database                                                                                                                                                                                                          
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases                                                                                                                                                     

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'testdb1',
        'USER': 'ankkamies',
        'PASSWORD': 'salainen',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization                                                                                                                                                                                              
# https://docs.djangoproject.com/en/1.6/topics/i18n/                                                                                                                                                                

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)                                                                                                                                                                            
# https://docs.djangoproject.com/en/1.6/howto/static-files/                                                                                                                                                         



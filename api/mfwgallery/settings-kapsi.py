""" 
Django settings for ankkabot project. For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see                                                                                                                                                                 
https://docs.djangoproject.com/en/1.6/ref/settings/                                                                                                                                                                 
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)                                                                                                                                             
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = '/home/users/ankkamies/sites/ankkamies.kapsi.fi/www/media/'
STATIC_ROOT = '/home/users/ankkamies/sites/ankkamies.kapsi.fi/www/static/'

MEDIA_URL = 'http://ankkamies.kapsi.fi/media/'
STATIC_URL = 'http://ankkamies.kapsi.fi/static/'

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
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mfwgallery.urls'

WSGI_APPLICATION = 'mfwgallery.wsgi.application'

# Database                                                                                                                                                                                                          
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases                                                                                                                                                     

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ankkamies',
        'USER': 'ankkamies',
        'PASSWORD': 'qWL4M27zq5',
        'HOST': 'psql1.n.kapsi.fi',
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



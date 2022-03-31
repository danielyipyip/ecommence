"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.shortcuts import reverse
from pathlib import Path
import django_heroku
import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media/')

# BASE_DIR = Path(__file__).resolve().parent.parent
# TEMPLATE_DIRS = [BASE_DIR / 'templates',]
# STATIC_DIRS = [BASE_DIR / 'static',]
# MEDIA_DIR = [BASE_DIR / 'media',]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@pbkh!#w%u-g7(k2newq1gt_2$yg#h#1qit6-+@5oloa!wh-#8'

# SECURITY WARNING: don't run with debug turned on in production!
# going to deploy -> change to False
DEBUG = False
#add to fix whitenise, suggested by: 
#https://stackoverflow.com/questions/51107962/static-file-issue-causing-django-500-error
DEBUG_PROPAGATE_EXCEPTIONS = True

#heroku: the online server (host), 127: local host, 
ALLOWED_HOSTS = ['danielyip-ecommerce.herokuapp.com', '127.0.0.1', 'localhost', 'www.jsblings.com', 'jsblings.com']


# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #django
    'django.contrib.sites',
    #own app
    'shop', 
    #third party
    #allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #social provider
    #'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter', 
    #for country field
    'django_countries',
    #forms
    'crispy_forms',
    #for AWS S3 online static file storage
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #add for deploy
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR+'/templates')],
        # 'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                #added allauth
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'NAME': str(BASE_DIR / 'db.sqlite3'),
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

# STATIC_ROOT=str(BASE_DIR / 'staticfiles')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATIC_URL = 'https://xxxxxxxxxxxxxx.cloudfront.net'
STATIC_URL = '/static/'

# STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
   ]

#https://stackoverflow.com/questions/59332225/hitting-500-error-on-django-with-debug-false-even-with-allowed-hosts
# STATICFILES_STORAGE = '.storage.WhiteNoiseStaticFilesStorage' # Read point 3 for details about this
#change to this one, it says after v4
#https://stackoverflow.com/questions/44160666/valueerror-missing-staticfiles-manifest-entry-for-favicon-ico
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'ecommerce.storage.WhiteNoiseStaticFilesStorage'
from whitenoise.storage import CompressedManifestStaticFilesStorage
class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

#media root: hold user upload files
MEDIA_ROOT=MEDIA_DIR
MEDIA_URL='/media/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

#authen redirect
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL='/shop/'
ACCOUNT_LOGOUT_REDIRECT_URL ='/shop/'
#LOGOUT_URL = '/shop/'

SOCIALACCOUNT_PROVIDERS = {
    #'facebook': {}, 
    'google':{}, 
    'twitter':{}}
#https://www.webforefront.com/django/setupdjangosocialauthentication.html
#https://testdriven.io/blog/django-social-auth/

#email stuffs (trying)


#https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab


#amazon AWS s3
AWS_ACCESS_KEY_ID=process.env.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=process.env.AWS_SECRET_KEY
AWS_STORAGE_BUCKET_NAME=process.env.AWS_BUCKET_NAME

#django storages
AWS_S3_FILE_OVERWRITE=False #overwirte file if same name? default=True
AWS_DEFAULT_ACL=None
DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3Boto3Storage'
#prioritize the s3 storage
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'#use this one (in API) does not work

#add by comments suggestion
AWS_S3_REGION_NAME ="us-east-2"
AWS_S3_ADDRESSING_STYLE = "virtual" #it said need if you're us-east-2 server

#after update django, it complained for default setup PK
DEFAULT_AUTO_FIELD='django.db.models.AutoField' 


#just try to add?
django_heroku.settings(locals())

# # force SSL rediect (may need paid dyno in Heroku)
# #from https://www.youtube.com/watch?v=CxrzD73r6Rw
if os.getcwd() == '/app': #if site is live
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True #forced redirect
    DEBUG = False

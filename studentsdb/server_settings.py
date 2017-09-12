import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['localhost', '<your domain>']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'students_db',
        'HOST': 'localhost',
        'USER': 'students_db_user',
        'PASSWORD': '<your password>',
     }
}

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
ADMIN_EMAIL = '<your admin email'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

# Social networks API (Facebook, Google+, Twitter)
FACEBOOK_KEY = ''
FACEBOOK_SECRET = ''
GOOGLE_OAUTH2_KEY = ''
GOOGLE_OAUTH2_SECRET = ''
TWITTER_KEY = ''
TWITTER_SECRET = ''


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '<path to static folder on your server>'

MEDIA_URL = '/media/'
MEDIA_ROOT = '<path to media folder on your server>'

ADMINS = (('<admin name>', '<admin email>'),)
MANAGERS = (('<manager name>', '<manager email>'),)

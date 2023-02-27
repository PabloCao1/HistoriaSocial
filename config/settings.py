from pathlib import Path
import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-nkd=f=s!(abn(-tan&ceplfpumy5#j$6v$hl_=5d@q)dni4477'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # aplicaciones django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',

    # aplicaciones de 3ros
    'crispy_forms',
    "crispy_bootstrap5",
    'django_extensions',

    # aplicaciones propias
    'Inicio',
    'Legajos',
    'Subs_PrimeraInfancia',
    'Subs_AsistenciaCritica',
    'Subs_0a18',
    'Subs_BienestarFamiliar',
    'Subs_PlanesSociales',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hsu_db',
#         'USER': 'root',
#         'PASSWORD': '123456',
#         'HOST':'localhost',
#         'PORT':'3306',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

#crispy-bootstrap5 0.6
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

#donde vamos a ir guardar los archivos medias debug
MEDIA_URL = "/media/"
#media para produccion
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

#esto se genera en producción y es la que deberemos 
#crear y django ira a buscar ahi 
#python manage.py collectstatic
STATIC_ROOT = BASE_DIR / 'static_root'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login 
LOGIN_URL = '/'
LOGIN_REDIRECT_URL= 'inicio/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_FORMS = {'login': 'user.forms.UserLoginForm'}

# #Configuracion para el envio de email por medio de GMAIL
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'CUENTAGOOGLE'
# # Clave generada desde la configuracion de Google
# EMAIL_HOST_PASSWORD = 'CONTRASEÑA DE APLICACION DE CUENTA GOOGLE' 
# RECIPIENT_ADDRESS = 'test@email.com'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-dark',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# GRAPH MODELS usado para automatizar la generacion de un DER de la BD
#  (ver más en: https://django-extensions.readthedocs.io/en/latest/graph_models.html)
GRAPH_MODELS = {
    # 'all_applications': True,
    # 'group_models': True,
    'app_labels': ["Inicio", "Legajos", "auth"],

}
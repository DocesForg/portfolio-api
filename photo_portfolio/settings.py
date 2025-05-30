"""
Django settings for photo_portfolio project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m(4bs8+r6pw_(d@f@k*gl*m#i-1f6&_!4v!bi98972jxrzne1+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# ВОТ ЗДЕСЬ ПРОПИСЫВАЕМ ДОМЕН БУДУЩЕГО САЙТА
ALLOWED_HOSTS = ['your-app-name.herokuapp.com','127.0.0.1']


# Application definition


# СОЗДАЮ ПРИЛОЖЕНИЕ С ФОТОГРАФИЯМИ + ФРЕЙМВОРК api для удобной работы с кодом
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'photos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'photo_portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'photo_portfolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# создаем папку где будут храниться фотки
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройте CORS для разрешения CORS-запросов к вашему API
INSTALLED_APPS += ['corsheaders']
# Добавьте CORS-заголовки в список промежуточных слоев для обработки CORS-запросов
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE

# Разрешить все домены (для разработки)
CORS_ALLOW_ALL_ORIGINS = True  
# или для продакшена:
# CORS_ALLOWED_ORIGINS = ["http://localhost:3000"] # Замените на ваш домен приложения



# Настройте Django REST framework для использования Django Filters
# Он позволяет применять фильтры к вашему API для поиска и сортировки данных
INSTALLED_APPS += ['django_filters']

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


# Установите настройки JWT для Django REST framework
# Они позволяют использовать JWT-токены для аутентификации пользователей в вашем API
INSTALLED_APPS += [
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'TOKEN_OBTAIN_SERIALIZER': 'photos.serializers.CustomTokenObtainPairSerializer',  # Указываем кастомный сериализатор
}
import os
from configparser import RawConfigParser


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

config = RawConfigParser()
config.read(os.path.join(BASE_DIR, "project", "settings.ini"))

SECRET_KEY = config.get("secrets", "secret_key")

DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        "HOST": config.get("database", "host"),
        "NAME": config.get("database", "name"),
        "PASSWORD": config.get("database", "password"),
        "PORT": config.get("database", "port"),
        "USER": config.get("database", "user"),
        "OPTIONS": {"autocommit": True}
    }
}

INSTALLED_APPS = (
    "django.contrib.staticfiles",
    "thermostat"
)

ROOT_URLCONF = "project.urls"
STATIC_URL = "/static/"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# FIXME: Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

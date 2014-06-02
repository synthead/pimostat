import os

from datetime import timedelta

from configparser import RawConfigParser


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

config = RawConfigParser()
config.read(os.path.join(BASE_DIR, "pimostat", "settings.ini"))


# Django settings.

SECRET_KEY = config.get("django", "secret_key")

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
    "pimostat"
)

ROOT_URLCONF = "pimostat.urls"
STATIC_URL = "/static/"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# FIXME: Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: don't run with debug turned on in production!

TEMPLATE_DEBUG = True
# FIXME
# ALLOWED_HOSTS = config.get("django", "allowed_hosts").replace(" ", "").split(
#     ",")


# Celery settings.

# Hack to make celery run in debug mode.
import sys
if "/usr/bin/celery" in sys.argv:
  DEBUG = False
else:
  DEBUG = True

CELERYBEAT_SCHEDULE = {
  "UpdateEnabledSensors": {
    "task": "pimostat.hardware_controller.UpdateEnabledSensors",
    # FIXME: Race condition if this is 1 second.
    "schedule": timedelta(seconds=10)
  }
}

BROKER_URL = config.get("celery", "broker_url")
CELERY_RESULT_BACKEND = config.get("celery", "result_backend")

CELERY_INCLUDE = ["pimostat.hardware_controller"]

CELERY_ACCEPT_CONTENT = ["pickle"]


# Pimostat settings.

PIMOSTAT_TESTING_WITHOUT_HARDWARE = config.getboolean(
    "celery", "testing_without_hardware")

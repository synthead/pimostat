import os

from configparser import RawConfigParser

from pimostat.celery import celery_pimostat

from celery.signals import celeryd_init
from celery.signals import worker_shutdown

from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


config = RawConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
config.read(os.path.join(BASE_DIR, "pimostat", "settings.ini"))

TESTING_WITHOUT_HARDWARE = config.getboolean(
    "celery", "testing_without_hardware")


@celeryd_init.connect
def CelerydInit(**kwargs):
  from celery.task.control import discard_all

  if not TESTING_WITHOUT_HARDWARE:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

  discard_all()


@worker_shutdown.connect
def WorkerShutdown(**kwargs):
  from pimostat.models import Relay

  for relay in Relay.objects.filter(enabled=True):
    ActuateRelay(relay, False)


@celery_pimostat.task
def UpdateEnabledSensors():
  from pimostat.models import Sensor

  for sensor in Sensor.objects.filter(enabled=True):
    # FIXME: Some strange race condition causes this: http://pastie.org/9238659
    # UpdateSensor.delay(sensor)
    UpdateSensor(sensor)


@celery_pimostat.task
def UpdateSensor(sensor):
  import re
  import decimal

  try:
    sensor_path = "/sys/bus/w1/devices/%s/w1_slave" % sensor.serial

    if TESTING_WITHOUT_HARDWARE:
      import random
      sensor_data = "t=%d" % random.randint(23000, 24000)
    else:
      with open(sensor_path) as sensor_file:
        sensor_data = sensor_file.read()

    match = re.search("t=(\d+)(\d{3})", sensor_data)
    if match:
      temperature = decimal.Decimal(".".join(match.groups()))
      if temperature != sensor.temperature:
        sensor.temperature = decimal.Decimal(".".join(match.groups()))
        sensor.save()

        logger.warning(
            "Updated sensor \"%s\" to %.3f degrees.", sensor.name,
            sensor.temperature)
    else:
      logger.error(
          "File \"%s\" contained unexpected data for sensor \"%s\"!  "
          "Disabling sensor!", sensor_path, sensor.name)
      sensor.enabled = False
      sensor.save()
  except FileNotFoundError:
    logger.error(
        "File \"%s\" not found for sensor \"%s\"!  Disabling sensor!",
        sensor_path, sensor.name)
    sensor.enabled = False
    sensor.save()
  except PermissionError:
    logger.error(
        "Permission denied to file \"%s\" for sensor \"%s\"!  Disabling "
        "sensor!", sensor_path, sensor.name)
    sensor.enabled = False
    sensor.save()


@celery_pimostat.task
def ActuateRelay(relay, actuated):
  if not TESTING_WITHOUT_HARDWARE:
    import RPi.GPIO as GPIO
    GPIO.setup(relay.channel, GPIO.OUT, initial=actuated)

  if relay.actuated is not actuated:
    relay.actuated = actuated
    relay.save()

    logger.warning(
        "Relay \"%s\" on channel %d %s.", relay.name, relay.channel,
        ("deactuated", "actuated")[relay.actuated])


@celery_pimostat.task
def CheckThermostats(**filter_args):
  from pimostat.models import Thermostat

  from django.db.models import F
  from django.db.models import Q

  for thermostat in Thermostat.objects.filter(Q(
      Q(Q(relay__actuated=True) & Q(
          Q(sensor__temperature__gte=F("desired_temperature") +
              F("upper_deviation")) |
          Q(enabled=False) |
          Q(relay__enabled=False) |
          Q(sensor__enabled=False))) |
      Q(Q(relay__actuated=False) & Q(
          Q(sensor__temperature__lte=F("desired_temperature") -
              F("lower_deviation")) &
          Q(enabled=True) &
          Q(relay__enabled=True) &
          Q(sensor__enabled=True)))),
      **filter_args):
    # Calling this with .delay() produces this error: http://pastie.org/9240631
    # ActuateRelay.delay(thermostat.relay, not thermostat.relay.actuated)
    ActuateRelay(thermostat.relay, not thermostat.relay.actuated)

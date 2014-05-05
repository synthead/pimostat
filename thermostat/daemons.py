from thermostat.models import Relay
from thermostat.models import Sensor
from thermostat.models import Thermostat

from django.db.models import F
from django.db.models import Q

import RPi.GPIO as GPIO
import re
import signal
import threading
import logging
import sys


class RelayGpio:
  def __init__(self, relay, actuated=True):
    self.relay = relay

    logging.info(
        "Initializing relay \"%s\" on channel %d.", relay.name, relay.channel)

    GPIO.setup(relay.channel, GPIO.OUT)
    self.Actuate(actuated)

  def Actuate(self, actuated):
    logging.info(
        "Setting relay \"%s\" on channel %d to %s.", self.relay.name,
        self.relay.channel, ["off", "on"][actuated])

    self.relay.actuated = actuated
    self.relay.save()
    GPIO.output(self.relay.channel, actuated)

  def CleanUp(self):
    if self.relay.actuated:
      self.Actuate(False)

    logging.info(
        "Stopping relay \"%s\" on channel %d.", self.relay.name,
        self.relay.channel)

    GPIO.cleanup(self.relay.channel)


def ReadSensorTemperature(serial):
  temperature_file = open("/sys/bus/w1/devices/%s/w1_slave" % serial)
  temperature_data = temperature_file.read()
  temperature_file.close()

  match = re.search("t=(\d+)", temperature_data)
  temperature = float(match.group(1)) / 1000

  return temperature


class ThermostatHardware:
  def __init__(self):
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        level=logging.INFO)

    GPIO.setmode(GPIO.BCM)

    self.active_relays = {}
    self.shutdown_requested = threading.Event()

    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT):
      signal.signal(sig, self.SignalHandler) 

  def SignalHandler(self, signal_number=None, frame=None):
    logging.info("Received signal %s.", signal_number)
    self.shutdown_requested.set()

  def UpdateLoop(self, interval=5):
    logging.info("Started thermostat daemon.")

    while not self.shutdown_requested.is_set():
      for sensor in Sensor.objects.filter(enabled=True):
        sensor.temperature = ReadSensorTemperature(sensor.serial)
        sensor.save()

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
              Q(sensor__enabled=True))))):
        logging.info(
            "Thermostat \"%s\" triggered by sensor \"%s\" at %.3f degrees.",
            thermostat.name, thermostat.sensor.name,
            thermostat.sensor.temperature)

        if not thermostat.relay.enabled:
          self.active_relays[thermostat.relay.pk].CleanUp()
          del self.active_relays[thermostat.relay.pk]
        elif thermostat.relay.pk not in self.active_relays:
          self.active_relays[thermostat.relay.pk] = RelayGpio(thermostat.relay)
        else:
          self.active_relays[thermostat.relay.pk].Actuate(
              not thermostat.relay.actuated)

        thermostat.relay.actuated = not thermostat.relay.actuated
        thermostat.save()

      self.shutdown_requested.wait(interval)

    for relay in self.active_relays.values():
      relay.CleanUp()

    logging.info("Stopped thermostat daemon.")


if __name__ == "__main__":
  ThermostatHardware().UpdateLoop()

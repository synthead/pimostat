from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from omnibus.api import publish

from pimostat.hardware_controller import CheckThermostats


class Relay(models.Model):
  name = models.CharField(default="Relay", max_length=255)
  enabled = models.BooleanField(default=True)
  channel = models.IntegerField(unique=True)
  actuated = models.BooleanField(default=False)

  class Meta:
    db_table = "relay"


class Sensor(models.Model):
  name = models.CharField(default="Sensor", max_length=255)
  enabled = models.BooleanField(default=True)
  serial = models.CharField(max_length=255, unique=True)
  temperature = models.DecimalField(max_digits=6, decimal_places=3, null=True)
  update_frequency = models.DecimalField(
      max_digits=4, decimal_places=1, default=5)

  class Meta:
    db_table = "sensor"


class Thermostat(models.Model):
  name = models.CharField(default="Thermostat", max_length=255)
  enabled = models.BooleanField(default=False)
  relay = models.ForeignKey(Relay, unique=True)
  sensor = models.ForeignKey(Sensor)
  desired_temperature = models.DecimalField(
      max_digits=6, decimal_places=3, default=16)
  lower_deviation = models.DecimalField(
      max_digits=6, decimal_places=3, default=0.5)
  upper_deviation = models.DecimalField(
      max_digits=6, decimal_places=3, default=0.3)

  class Meta:
    db_table = "thermostat"


@receiver(post_save, sender=Thermostat)
def ThermostatUpdated(sender, **kwargs):
  CheckThermostats.delay()


@receiver(post_save, sender=Sensor)
def SensorUpdated(sender, **kwargs):
  CheckThermostats.delay(sensor=kwargs["instance"])
  if kwargs["instance"].temperature is not None:
    kwargs["instance"].temperature = float(kwargs["instance"].temperature)

  publish(
      "pimostat", "sensor-%d" % kwargs["instance"].pk,
      {"temperature": kwargs["instance"].temperature})


@receiver(post_save, sender=Relay)
def RelayUpdated(sender, **kwargs):
  publish(
      "pimostat", "relay-%d" % kwargs["instance"].pk,
      {"actuated": str(kwargs["instance"].actuated)})

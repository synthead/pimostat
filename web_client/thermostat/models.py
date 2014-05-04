from django.db import models


class Relay(models.Model):
  channel = models.IntegerField(unique=True)
  state = models.NullBooleanField()
  enabled = models.BooleanField(default=False)


class Sensor(models.Model):
  serial = models.CharField(max_length=255, unique=True)
  temperature = models.DecimalField(max_digits=6, decimal_places=3, null=True)
  enabled = models.BooleanField(default=False)


class Thermostat(models.Model):
  relay = models.ForeignKey(Relay)
  sensor = models.ForeignKey(Sensor)
  desired_temperature = models.DecimalField(
      max_digits=6, decimal_places=3, null=True)
  lower_deviation = models.DecimalField(
      max_digits=6, decimal_places=3, default=0.5)
  upper_deviation = models.DecimalField(
      max_digits=6, decimal_places=3, default=0.5)
  enabled = models.BooleanField(default=False)
from django.db import models


class Relay(models.Model):
  name = models.CharField(max_length=255)
  channel = models.IntegerField(unique=True)
  actuated = models.BooleanField()
  enabled = models.BooleanField()


class Sensor(models.Model):
  name = models.CharField(max_length=255)
  serial = models.CharField(max_length=255, unique=True)
  temperature = models.DecimalField(max_digits=6, decimal_places=3, null=True)
  enabled = models.BooleanField()


class Thermostat(models.Model):
  name = models.CharField(max_length=255)
  relay = models.ForeignKey(Relay)
  sensor = models.ForeignKey(Sensor)
  desired_temperature = models.DecimalField(
      max_digits=6, decimal_places=3, null=True)
  lower_deviation = models.DecimalField(
      max_digits=6, decimal_places=3, default=0.5)
  upper_deviation = models.DecimalField(
      max_digits=6, decimal_places=3, default=0.5)
  enabled = models.BooleanField()

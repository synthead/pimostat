from django.forms import ModelForm

from pimostat.models import Thermostat


class ThermostatForm(ModelForm):
  class Meta:
    model = Thermostat
    fields = [
        "desired_temperature",
        "enabled"
    ]

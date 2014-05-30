from django.forms import ModelForm

from thermostat.models import Thermostat


class ThermostatForm(ModelForm):
  class Meta:
    model = Thermostat
    fields = [
        "desired_temperature",
        "enabled"
    ]

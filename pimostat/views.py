from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.forms.models import modelformset_factory

from pimostat.models import Relay
from pimostat.models import Sensor
from pimostat.models import Thermostat

from pimostat.forms import ThermostatForm


ThermostatModelFormSet = modelformset_factory(
    Thermostat, form=ThermostatForm, extra=0)


def Index(request):
  context = {"thermostat_formset": ThermostatModelFormSet}
  return render(request, "index.html", context)


def UpdateThermostat(request):
  thermostat_formset = ThermostatModelFormSet(request.POST)
  thermostat_formset.save()
  return HttpResponse("Submitted.")


def GetTemperature(request, pk=None):
  try:
    sensor = Sensor.objects.get(pk=pk)
    return HttpResponse(sensor.temperature)
  except DoesNotExist:
    return HttpResponseServerError(
        "Sensor with primary key %d does not exist." % pk)

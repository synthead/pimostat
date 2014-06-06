import json

from django.core.serializers.json import DjangoJSONEncoder

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
  context = {
      "thermostat_formset": ThermostatModelFormSet,
  }
  return render(request, "index.html", context)


def UpdateThermostat(request):
  thermostat_formset = ThermostatModelFormSet(request.POST)
  thermostat_formset.save()

  return HttpResponse("Submitted.")


def PollThermostat(request, pk=None):
  try:
    thermostat = Thermostat.objects.get(pk=pk)
    json_response = json.dumps({
        "temperature": thermostat.sensor.temperature,
        "actuated": thermostat.relay.actuated
    }, cls=DjangoJSONEncoder)
    return HttpResponse(json_response)
  except Thermostat.DoesNotExist:
    return HttpResponseServerError(
        "Sensor with primary key %d does not exist." % pk)

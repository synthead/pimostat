from django.shortcuts import render
from django.http import HttpResponse

from thermostat.models import Relay
from thermostat.models import Sensor
from thermostat.models import Thermostat

from thermostat.forms import ThermostatForm


def Index(request):
  forms = [ThermostatForm(instance=t) for t in Thermostat.objects.all()]
  context = {
      "forms": forms
  }
  return render(request, "index.html", context)


def UpdateThermostat(request, pk=None):
  # FIXME: check for post
  thermostat = Thermostat.objects.get(pk=pk)
  form = ThermostatForm(request.POST, instance=thermostat)
  # FIXME: validate
  form.save()
  return HttpResponse("Submitted.")

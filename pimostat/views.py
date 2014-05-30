from django.shortcuts import render
from django.http import HttpResponse

from pimostat.models import Relay
from pimostat.models import Sensor
from pimostat.models import Thermostat

from pimostat.forms import ThermostatForm


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

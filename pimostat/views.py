import json

from django.shortcuts import render
from django.http import HttpResponse

from django.forms.models import modelformset_factory
from pimostat.forms import ThermostatForm

from pimostat.models import Thermostat


ThermostatModelFormSet = modelformset_factory(
    Thermostat, form=ThermostatForm, extra=0)


def Index(request):
  context = {"thermostat_formset": ThermostatModelFormSet}

  return render(request, "index.html", context)


def UpdateThermostat(request):
  thermostat_formset = ThermostatModelFormSet(request.POST)
  thermostat_formset.save()

  return HttpResponse("Submitted.")

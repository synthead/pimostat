from django.conf.urls import patterns
from django.conf.urls import url

from pimostat import views


urlpatterns = patterns("",
  url(r"^$", views.Index),
  url(r"^update_thermostat$", views.UpdateThermostat)
)

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from pimostat import views


urlpatterns = patterns("",
  url(r"^$", views.Index, name="index"),
  url(r"^forms/update_thermostat$", views.UpdateThermostat,
      name="update_thermostat"),
  url(r"^get_temperature/(?P<pk>\d+)$", views.GetTemperature,
      name="get_temperature")
)

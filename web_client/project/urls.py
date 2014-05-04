from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from thermostat import views


urlpatterns = patterns("",
  url(r"^$", views.Index, name="index"),
  url(r"^forms/update_thermostat/(?P<pk>\d+)$", views.UpdateThermostat,
      name="update_thermostat")
)

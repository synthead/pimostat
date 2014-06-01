from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from pimostat import views


urlpatterns = patterns("",
  url(r"^$", views.Index),
  url(r"^update_thermostat$", views.UpdateThermostat),
  url(r"^poll_thermostat/(?P<pk>\d+)$", views.PollThermostat)
)

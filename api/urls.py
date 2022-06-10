from django.urls import URLPattern, path, include
from . import views


urlpatterns = [
    path('',views.index),
    path('check_device_class',views.check_device_class),
    path('add_relay_log',views.add_relay_log),
    path('check_relay_trigger',views.check_relay_trigger),
    path('add_sensor_log',views.add_sensor_log),
]
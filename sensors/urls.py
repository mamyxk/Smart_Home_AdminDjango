from django.urls import URLPattern, path, include
from . import views


urlpatterns = [
    path('',views.sensors_list),
    path('create-sensor/',views.create_sensor),
    path('edit-sensor/<int:sensor_id>/',views.edit_sensor),
    path('types/',views.list_sensorTypes)
]
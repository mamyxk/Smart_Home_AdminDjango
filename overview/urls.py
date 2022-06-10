from django.urls import URLPattern, path, include
from . import views


urlpatterns = [
    path('',views.index),
    path('sensors/',include('sensors.urls')),
    path('relays/',include('relays.urls')),
    path('triggers/',include('triggers.urls')),
]
from django.urls import URLPattern, path, include
from . import views


urlpatterns = [
    path('',views.relays_list),
    path('create-relay/',views.create_relay),
    path('types/',views.list_RelayTypes),
    path('create-type/',views.create_type),
    path('edit-relay/<int:relay_id>/<int:relay_bus>/',views.edit_relay_trigger),
    path('edit-relay/<int:relay_id>/<int:relay_bus>/create_bus_trigger/',views.create_relay_trigger_bus),
    path('edit-relay/<int:relay_id>/<int:relay_bus>/edit_bus_trigger/',views.edit_relay_trigger_bus),
    path('edit-relay/<int:relay_id>/<int:relay_bus>/edit_bus_trigger_time/',views.edit_bus_trigger_time),


]
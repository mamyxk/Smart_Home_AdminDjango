from dataclasses import fields
from importlib.util import spec_from_file_location
from select import select
from rest_framework import serializers

from triggers.models import Triggers, TimeTriggers, UserTriggers, RelayTriggers
from relays.models import *
from sensors.models import *

class RelayState(serializers.FileField):
    def to_representation(self, value):
        return 4

class RelayLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayLogs
        fields = ["hwid"]

class CheckDeviceClassSerializer(serializers.Serializer):
    hwid = serializers.IntegerField()
    device_class = serializers.SerializerMethodField()

    def get_device_class(self,obj):
        res = ""
        total_device_found = 0
        if len(RelayDevices.objects.filter(hwid=obj["hwid"])) > 0:
            total_device_found+=1
            res = "Relay_Device"
        if len(SensorDevices.objects.filter(hwid=obj["hwid"])) > 0:
            total_device_found+=1
            res = SensorDevices.objects.get(hwid=obj["hwid"]).type_id.name
            # res = "Sensor_Device"
        # return len(RelayDevices.objects.filter(hwid=obj["hwid"]))
        if total_device_found == 1:
            return res
        elif total_device_found == 0:
            return None
        else:
            return "Error"


class RelayTriggerFulfilledSerializer(serializers.Serializer):
    hwid = serializers.IntegerField()
    bus = serializers.IntegerField()
    fulfilled = serializers.SerializerMethodField()

    # obj -> "OrderedDict([('hwid', 1), ('bus', 3)])"
    def get_fulfilled(self, obj):
        try:
            requested_device = RelayDevices.objects.get(hwid=obj["hwid"])
            requested_device_id = requested_device.id
            requested_relay_trigger = RelayTriggers.objects.get(relay_id = requested_device_id, bus = obj["bus"])
            # requested_trigger = requested_relay_trigger.trigger_id
            return requested_relay_trigger.isfulfilled()
        except (RelayDevices.DoesNotExist,RelayTriggers.DoesNotExist) as err :
            return None

class SensorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorLogs
        fields = ('sensor_id','data_type','value','created_at')

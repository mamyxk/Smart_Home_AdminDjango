from dataclasses import field
from .models import *
from django import forms
from .models import *

class SensorIdToString(forms.ModelChoiceField):
    def label_from_instance(self, obj) -> str:
        return str(obj.name)

class CreateSensorForm(forms.ModelForm):
    type_id = SensorIdToString(queryset=SensorTypes.objects.all())
    class Meta:
        model = SensorDevices
        fields = ['hwid','type_id','name','description']

class EditSensorForm(forms.ModelForm):
    type_id = SensorIdToString(queryset=SensorTypes.objects.all())
    class Meta:
        model = SensorDevices
        fields = ['type_id','hwid','name','description']
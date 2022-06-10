from dataclasses import fields
from django import forms
from django.forms import ModelChoiceField
from .models import RelayDevices, RelayTypes

class CustomTypeIdChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj) -> str:
        return str(obj.name)

class AddRelayDeviceForm(forms.ModelForm):
    type_id = CustomTypeIdChoiceField(queryset=RelayTypes.objects.all())
    class Meta:
        model = RelayDevices
        fields = ['type_id','hwid','name','description']

class AddDeviceTypeForm(forms.Form):
    class Meta:
        model = RelayTypes
        fields = ['name','buses','description']

class EditRelayForm(forms.ModelForm):
    type_id = CustomTypeIdChoiceField(queryset=RelayTypes.objects.all())
    class Meta:
        model = RelayDevices
        fields = ['hwid','name','description','type_id']
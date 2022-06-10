from dataclasses import fields
from django import forms

from triggers.models import *

# class Create_Relay_Trigger_Bus_Form(forms.ModelForm):
#     def __init__(self,relay_id,relay_bus,*args,**kwargs):
#         self.relay_id = relay_id
#         self.relay_bus = relay_bus
#         super(Create_Relay_Trigger_Bus_Form,self).__init__(*args,**kwargs)
#     class Meta:
#         model = RelayTriggers
#         fields = []


class Edit_Relay_Trigger_Form(forms.ModelForm):
    class Meta:
        model = RelayTriggers
        fields = ["force_state"]

class EditTimeTriggerForm(forms.ModelForm):
    class Meta:
        model = TimeTriggers
        fields = ["start_time", "end_time"]
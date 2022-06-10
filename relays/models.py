from django.db import models
from devices.models import Device
# Create your models here.

class RelayTypes(models.Model):
    name = models.CharField(max_length=20)
    buses = models.IntegerField(default = None, null=True)
    description = models.TextField(max_length=300)

class RelayDevices(Device):
    type_id = models.ForeignKey('RelayTypes', on_delete=models.PROTECT)
    class Meta:
        ordering = ['hwid','name','description','type_id']

    # def get_id(self):
    #     return self.id

    def get_name(self):
        return self.name

class RelayLogs(models.Model):
    sensor_id = models.ForeignKey('RelayDevices',on_delete=models.PROTECT)
    bus = models.IntegerField(default = None, null=True)
    value = models.BooleanField(default=None, null=True)
    create_at = models.DateTimeField()
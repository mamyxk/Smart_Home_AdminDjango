from email.policy import default
from multiprocessing.sharedctypes import Value
from django.db import models
from devices.models import Device

# Create your models here.

class SensorDataType(models.Model):
    name = models.CharField(max_length=20)

class SensorInputTypes(models.Model):
    type_id = models.ForeignKey('SensorTypes', on_delete=models.PROTECT)
    data_id = models.ForeignKey('SensorDataType',on_delete=models.PROTECT)
    precision = models.FloatField(null=True)

class SensorTypes(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=300)

class SensorDevices(Device):
    type_id = models.ForeignKey('SensorTypes', on_delete=models.PROTECT)
    class Meta:
        ordering = ['hwid','name','description','type_id']

class SensorLogs(models.Model):
    sensor_id = models.ForeignKey('SensorDevices',on_delete=models.PROTECT)
    data_type = models.ForeignKey('SensorDataType',on_delete=models.PROTECT)
    value = models.FloatField(default=None, null=True)
    created_at = models.DateTimeField()
    
from django.db import models

# Create your models here.

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    hwid = models.IntegerField(default = None, null=True,unique=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=300)
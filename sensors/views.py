from django.http import HttpResponse
from django.shortcuts import redirect, render

from triggers.forms import Edit_Relay_Trigger_Form
from .models import SensorDevices
from .forms import *

# Create your views here.

def sensors_list(request):
    # all_devices = SensorDevices.objects.filter()
    all_devices = SensorDevices.objects.filter().prefetch_related('type_id').select_related('type_id')
    print(all_devices.query)
    print('-------------------')
    # print(type(all_devices))
    cntxt = {"all_devices": all_devices}

    return render(request,'sensors/sensors_list.html', context=cntxt)

def create_sensor(request):
    cntxt = {}
    if request.method == 'POST':
        create_sensor_form = CreateSensorForm(request.POST)
        if create_sensor_form.is_valid():
            create_sensor_form.save()
            return redirect('/sensors')
    else:
        create_sensor_form = CreateSensorForm()
        cntxt['create_sensor_form'] = create_sensor_form
    return render(request,'sensors/create_sensor.html',context=cntxt)

def edit_sensor(request,sensor_id):
    cntxt = {}
    try:
        sensor_to_edit = SensorDevices.objects.get(id=sensor_id)
        if request.method == 'POST':
            edit_sensor_form = EditSensorForm(request.POST,instance=sensor_to_edit)
            if edit_sensor_form.is_valid():
                edit_sensor_form.save()
        else:    
            edit_sensor_form = EditSensorForm(instance=sensor_to_edit)
        cntxt['edit_sensor_form'] = edit_sensor_form

        return render(request,'sensors/edit_sensor.html',context=cntxt)
    except (SensorDevices.DoesNotExist) as err:
        return HttpResponse(err)

def list_sensorTypes(request):
    all_types = SensorTypes.objects.filter()
    cntxt = {"all_types": all_types}
    return render(request,'sensors/sensor_types_list.html',context=cntxt)
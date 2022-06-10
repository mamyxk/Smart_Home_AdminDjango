from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from .models import RelayDevices
from triggers.models import *
from triggers.forms import *
from .forms import AddRelayDeviceForm, AddDeviceTypeForm, EditRelayForm

# Create your views here.


def relays_list(request):
    all_devices = RelayDevices.objects.filter()

    cntxt = {"all_devices": all_devices}
    return render(request, 'relays/relays_list.html', context=cntxt)


def create_relay(request):
    cntxt = {}
    if request.method == 'POST':
        create_relay_form = AddRelayDeviceForm(request.POST)
        if create_relay_form.is_valid():
            create_relay_form.save()
            return redirect('/relays')
        else:
            None
            # TODO handle wrong data at form
    else:
        create_relay_form = AddRelayDeviceForm()
        cntxt['create_relay_form'] = create_relay_form
    return render(request, 'relays/add_relay.html',context=cntxt)


def list_RelayTypes(request):
    all_types = RelayTypes.objects.filter()
    cntxt = {"all_types": all_types}
    return render(request, 'relays/relay_types_list.html',context=cntxt)


def create_type(request):
    return render(request, 'relays/relays.html')


def edit_relay_trigger(request,relay_id, relay_bus):

    try:
        relay_to_edit = RelayDevices.objects.get(id=relay_id)
        if request.method == 'POST':
            req_edit_relay_bus_form = EditRelayForm(request.POST,instance=relay_to_edit)
            if req_edit_relay_bus_form.is_valid():
                req_edit_relay_bus_form.save()
            
        cntxt = {
            "relay_id" : relay_id,
            "relay_to_edit": relay_to_edit,
        }
        relay_to_edit_bus_count=relay_to_edit.type_id.buses
        relay_buses_btns = []
        for i in range(0,relay_to_edit_bus_count,1):
            relay_buses_btns.append((i,i+1))
        cntxt["relay_buses_btns"] = relay_buses_btns

        cntxt["relay_to_edit_buses"] = relay_to_edit_bus_count

        edit_relay_form = EditRelayForm(instance=relay_to_edit)
        cntxt["edit_relay_form"] = edit_relay_form

    except (RelayDevices.DoesNotExist) as err:
        # Relay or Relay Trigger does not exist
        print(err)
        return HttpResponse(str(err))
    # Relay Triggers Buses
    try:
        bus_trigger = RelayTriggers.objects.get(relay_id=relay_id,bus=relay_bus)
        edit_relay_bus_form = Edit_Relay_Trigger_Form(instance=bus_trigger)
        cntxt["edit_relay_bus_form"] = edit_relay_bus_form
    except (RelayTriggers.DoesNotExist) as err:
        bus_trigger = None

    

    if bus_trigger != None:
        trigger_instance = bus_trigger.trigger_id
        try:
            time_trigger_instance = TimeTriggers.objects.get(trigger_id=trigger_instance)
        except (TimeTriggers.DoesNotExist) as err:
            time_trigger_instance = None
            print(err)
        if time_trigger_instance is None:
            edit_time_trigger_form = EditTimeTriggerForm()
        else:
            edit_time_trigger_form = EditTimeTriggerForm(instance=time_trigger_instance)
        cntxt["edit_time_trigger_form"] = edit_time_trigger_form
    
    # return HttpResponse(str(cntxt["edit_relay_form"]))
    return render(request, 'relays/edit_relay.html', cntxt)

def create_relay_trigger_bus(request,relay_id, relay_bus):
    try:
        relay_device = RelayDevices.objects.get(id=relay_id)
        if request.method == 'POST':
            trig_new = Triggers.objects.create(child_modes='OR',parent_id=None,active=True)
            RelayTriggers.objects.create(relay_id=relay_device,bus=relay_bus,trigger_id = trig_new)
           
    except (RelayDevices.DoesNotExist) as err:
        print(err)    
    return redirect(f"/relays/edit-relay/{relay_id}/{relay_bus}/")

def edit_relay_trigger_bus(request,relay_id, relay_bus):
    try:
        relay_device = RelayDevices.objects.get(id=relay_id)
        trigger_instance = RelayTriggers.objects.get(relay_id=relay_device,bus=relay_bus)
        if request.method == 'POST':
            edit_trigger_instance = Edit_Relay_Trigger_Form(request.POST,instance=trigger_instance)
            if edit_trigger_instance.is_valid():
                edit_trigger_instance.save()
    except (RelayDevices.DoesNotExist,RelayTriggers.DoesNotExist) as err:
        print(err)    
    return redirect(f"/relays/edit-relay/{relay_id}/{relay_bus}/")

def edit_bus_trigger_time(request,relay_id, relay_bus):
    # return HttpResponse("here")
    try:
        relay_device = RelayDevices.objects.get(id=relay_id)
        relay_trigger_instance = RelayTriggers.objects.get(relay_id=relay_device,bus=relay_bus)
    except (RelayDevices.DoesNotExist,RelayTriggers.DoesNotExist) as err:
        print(err)
        relay_trigger_instance = None
    
    if relay_trigger_instance is None:
        return redirect(f"/relays/edit-relay/{relay_id}/{relay_bus}/")

    try:
        trigger_instance = relay_trigger_instance.trigger_id
        time_trigger_instance = TimeTriggers.objects.get(trigger_id=trigger_instance.id)
    except (TimeTriggers.DoesNotExist) as err:
        time_trigger_instance = None
        print(err)

    if time_trigger_instance is None:
        time_trigger_instance = TimeTriggers.objects.create(trigger_id=trigger_instance,start_time='00:00:00.000',end_time='00:00:00.000')
    if request.method == 'POST':
        edit_time_trigger_form = EditTimeTriggerForm(request.POST,instance=time_trigger_instance)
        if edit_time_trigger_form.is_valid():
            edit_time_trigger_form.save()
            print("Was valid")
        else:
            print("was not valid")
        return redirect(f"/relays/edit-relay/{relay_id}/{relay_bus}/")



    return redirect(f"/relays/edit-relay/{relay_id}/{relay_bus}/")
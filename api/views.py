from re import S
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
import io
from rest_framework.parsers import JSONParser

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from tomlkit import datetime

import relays.models as relmod
from .serializers import *

import datetime

# Create your views here.

def index(request):
    return HttpResponse("Api INDEX")


def relay(request):
    return HttpResponse("Hello world")

@api_view(['POST'])
def check_device_class(request):
    if request.method == 'POST':
        serializer = CheckDeviceClassSerializer(data = request.data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(data=None,status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def add_relay_log(request):
    if request.method == 'POST':
        serializer = RelayLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_relay_trigger(request):
    if request.method == 'POST':
        serializer = RelayTriggerFulfilledSerializer(data = request.data)
        if serializer.is_valid():
            # return HttpRequest(serializer.data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(data=None,status=status.HTTP_405_METHOD_NOT_ALLOWED)

# hwdid, data_type, value
@api_view(['POST'])
def add_sensor_log(request):
    if request.method == 'POST':
        print(request.body)
        json_data = json.loads(request.body)
        try:
            json_data["sensor_id"] = SensorDevices.objects.get(hwid=json_data["hwid"]).id
            json_data["created_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except TypeError as err:
            return HttpResponse(err)
        del json_data["hwid"]
        serializer = SensorLogSerializer(data=json_data)
        if serializer.is_valid():
            serializer.save()
            print("valid")
        else:
            print(serializer.errors)
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    # return Response(serializer.errors,status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return JsonResponse(json_data)
    
    # if request.method == 'POST':
    #     json_data = json.loads(request.body)
    #     try:
    #         hwid = json_data["hwid"]
    #         device_id = SensorDevices.objects.get(hwid=hwid)
    #         json_data["sensor_id"] = device_id
    #         type_id = SensorDataType.objects.get(id=json_data["data_type"])
    #         json_data["data_type"] = type_id
    #         del json_data["hwid"]
    #         SensorLogs.objects.create(**json_data)
    #         return JsonResponse(json_data)
    #     except TypeError as err:
    #         return HttpResponse(err)

        
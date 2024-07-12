from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from ninja import NinjaAPI
from .models import Device, Location
from .schemas import DeviceSchema, LocationSchema



app = NinjaAPI()


@app.get("devices/", response=list[DeviceSchema])
def list_devices(request: HttpRequest):
    return Device.objects.all()


@app.get("devices/{slug}/", response=DeviceSchema)
def get_device(request: HttpRequest, slug: str):
    return get_object_or_404(Device, slug=slug)


@app.get("locations/", response=list[LocationSchema])
def list_locations(request: HttpRequest):
    return Location.objects.all()
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI

from .models import Device, Location
from .schemas import (
    DeviceCreateSchema,
    DeviceLocationPatch,
    DeviceSchema,
    Error,
    LocationSchema,
)

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


@app.post("devices/", response={200: DeviceSchema, 404: Error})
def create_device(request: HttpRequest, device: DeviceCreateSchema):
    if device.location_id is not None:
        location_exists = Location.objects.filter(id=device.location_id).exists()

        if not location_exists:
            return 404, {"message": "Location not found"}

    return Device.objects.create(**device.model_dump())


@app.patch(
    "devices/{device_slug}/set-location/", response={200: DeviceSchema, 404: Error}
)
def update_device_location(
    request: HttpRequest, device_slug: str, data: DeviceLocationPatch
):
    device = get_object_or_404(Device, slug=device_slug)
    
    if data.location_id is not None:
        device.location = get_object_or_404(Location, id=data.location_id)
    else:
        device.location = None
    
    device.save()
    return device

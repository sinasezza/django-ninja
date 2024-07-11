from django.contrib import admin
from .models import Device, Location


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass

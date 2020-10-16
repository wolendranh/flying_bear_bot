# -*- coding: utf-8 -*-
from django.contrib import admin
from snow_camera.models import Location, Camera


class CameraAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Location, LocationAdmin)
admin.site.register(Camera, CameraAdmin)

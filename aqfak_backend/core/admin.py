from django.contrib import admin
from .models import Crop,CropSchedule,CropSensorData

admin.site.register(Crop)
admin.site.register(CropSensorData)
admin.site.register(CropSchedule)

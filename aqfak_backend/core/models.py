from django.db import models
from user_auth.models import CustomUser

# Create your models here.

class Crop(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    stage =models.TextField(max_length=50)
    area =models.TextField(max_length=50)
    grown = models.CharField(max_length=20,null=True, blank=True)
    def __str__(self):
        return self.name
    

#new tables
class CropSensorData(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20, default = 'normal')
    ph = models.FloatField()
    phStatus = models.CharField(max_length=20, default = 'optimal')
    nitrogen = models.SmallIntegerField()
    phosphorous = models.SmallIntegerField()
    potassium = models.SmallIntegerField()

    def __str__(self):
        return f"Crop: {self.crop}, pH: {self.ph}"

class CropSchedule(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    activity = models.CharField(max_length=25)
    description = models.TextField(max_length=100,null=True, blank=True)
    time = models.DateTimeField()

    def __str__(self):
        return f"Crop: {self.crop}, Activity: {self.activity}"
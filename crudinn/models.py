from django.db import models
from registration.models import CustomUser

# Create your models here.
class InnModel(models.Model):
    inn_id = models.BigAutoField(primary_key=True,)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="username",)
    address = models.CharField(null=False, max_length=250, blank=True,)
    description = models.CharField(null=False, max_length=250, blank=True,)
    date = models.DateField()
    active = models.BooleanField(null=False, default=True)
    anonymization = models.BooleanField(null=False, default=False)
    
class InnImageModel(models.Model):
    inn_image_id = models.ForeignKey(InnModel, on_delete=models.CASCADE, to_field="inn_id",)
    image = models.ImageField(upload_to="inn_images", null=False)
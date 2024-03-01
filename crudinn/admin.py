from django.contrib import admin
from .models import InnModel, InnImageModel

# Register your models here.
admin.site.register(InnModel)
admin.site.register(InnImageModel)
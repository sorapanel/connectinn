from django.contrib import admin
from .models import ApplyInnModel, ChatModel, ChatContentModel

# Register your models here.
admin.site.register(ApplyInnModel)
admin.site.register(ChatModel)
admin.site.register(ChatContentModel)
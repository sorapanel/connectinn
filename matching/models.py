from django.db import models
from registration.models import CustomUser
from crudinn.models import InnModel

# Create your models here.
class ApplyInnModel(models.Model):
    apply_inn_id =  models.BigAutoField(primary_key=True,)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="username", related_name='host_applyinnmodels',)
    guest = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="username", related_name='guest_applyinnmodels',)
    info = models.CharField(null=False, blank=True, max_length=500,)
    phone_num = models.CharField(null=False, blank=False, max_length=250,)
    inn_id = models.ForeignKey(InnModel, on_delete=models.CASCADE, to_field="inn_id",)
    active = models.BooleanField(null=False, default=False)

class ChatModel(models.Model):
    chat_id = models.BigAutoField(primary_key=True,)
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="username", related_name='user1_chatmodels',)
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="username", related_name='user2_chatmodels',)

class ChatContentModel(models.Model):
    chat_content_id = models.ForeignKey(ChatModel, on_delete=models.CASCADE, to_field="chat_id",)
    contents =  models.CharField(null=False, blank=True, max_length=500,)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="username",)
    created_at = models.DateTimeField(auto_now_add=True)
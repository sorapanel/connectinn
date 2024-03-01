from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from crudinn.models import InnModel,InnImageModel
from .forms import ApplyInnForm, SendForm, SearchForm
from .models import ApplyInnModel, ChatModel, ChatContentModel
from registration.models import CustomUser
from django.urls import reverse_lazy

# Create your views here.
class SearchInn(TemplateView):
    template_name = "matching/search_inn.html"
    form_class = SearchForm

    def get(self, request):
        inn_instances = []
        inn_images = []
        inn_images_instances = []
        form = self.form_class()

        inn_instances = InnModel.objects.filter(active=True)

        for inn_instance in inn_instances:
            images = InnImageModel.objects.filter(inn_image_id=inn_instance)
            inn_instance.address = anonymizationCheck(inn_instance)
            inn_images.append(inn_instance)
            for image in images:
                inn_images.append(image)
            inn_images_instances.append(inn_images)
            inn_images = []
                
        return render(request, "matching/search_inn.html", {"instances": inn_images_instances, "form":form,})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            address = str(address).replace(" ","")

            inn_instances = []
            inn_images = []
            inn_images_instances = []
            form = self.form_class()

            inns = InnModel.objects.filter(active=True)

            for inn in inns:
                if address in inn.address:
                    inn_instances.append(inn)

            for inn_instance in inn_instances:
                images = InnImageModel.objects.filter(inn_image_id=inn_instance)
                inn_instance.address = anonymizationCheck(inn_instance)
                inn_images.append(inn_instance)
                for image in images:
                    inn_images.append(image)
                inn_images_instances.append(inn_images)
                inn_images = []

        return render(request, "matching/search_inn.html", {"instances": inn_images_instances, "form":form,})
        
    
class ApplyInn(TemplateView):
    template_name = "matching/apply_inn.html"
    form_class = ApplyInnForm

    def get(self, request):
        param = request.GET.get("param")
        inn_instance = InnModel.objects.get(pk = param)
        inn_instance.address = anonymizationCheck(inn_instance)
        inn_images_instances = InnImageModel.objects.filter(inn_image_id = inn_instance)
        form = self.form_class()

        return render(request, "matching/apply_inn.html", {"form":form, "inn_instance":inn_instance, "inn_images_instances":inn_images_instances})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            info = form.cleaned_data['info']
            phone_num = form.cleaned_data['phone_num']
            username = request.session.get('username', None)
            inn_id = request.POST.get("inn_id")

            inn_instance = InnModel.objects.get(inn_id=inn_id)

            guest_userinstance = CustomUser.objects.get(username=username["username"])

            ApplyInnModel.objects.create(host=inn_instance.username, guest=guest_userinstance, info=info, phone_num=phone_num, inn_id=inn_instance)

            return redirect("registration:index")
        else:
            print(form.errors)
        return redirect("matching:search_inn")
    
def permitApply(request):
    param = request.GET.get("param")
    apply_inn_instance = ApplyInnModel.objects.get(apply_inn_id=param)
    apply_inn_instance.active = True
    inn_instance = InnModel.objects.get(inn_id=apply_inn_instance.inn_id.inn_id)
    inn_instance.active = False
    apply_inn_instance_others = ApplyInnModel.objects.filter(inn_id=apply_inn_instance.inn_id)
    for apply_inn_instance_other in apply_inn_instance_others:
        apply_inn_instance_other.delete()
    apply_inn_instance.save()
    inn_instance.save()

    guest_userinstance = apply_inn_instance.guest

    if inn_instance.username.pk > guest_userinstance.pk:
        try:
            ChatModel.objects.get(user1=inn_instance.username, user2=guest_userinstance)
        except:
                    ChatModel.objects.create(user1=inn_instance.username, user2=guest_userinstance)
    else:
        try:
            ChatModel.objects.get(user2=inn_instance.username, user1=guest_userinstance)
        except:
            ChatModel.objects.create(user2=inn_instance.username, user1=guest_userinstance)

    return redirect("registration:index")

def cancelApply(request):
    param = request.GET.get("param")
    apply_inn_instance = ApplyInnModel.objects.get(apply_inn_id=param)
    inn_instance = InnModel.objects.get(inn_id=apply_inn_instance.inn_id.inn_id)
    inn_instance.active = True
    apply_inn_instance.delete()
    inn_instance.save()
    return redirect("registration:index")

class AppliedInn(TemplateView):
    template_name="matching/applied_inn.html"

    def get(self, request):
        params = []
        username = request.session.get("username", None)
        user_instance = CustomUser.objects.get(username=username["username"])
        apply_inn_instaces  = ApplyInnModel.objects.filter(active=True, host=user_instance)

        for apply_inn_instance in apply_inn_instaces:
            info = {"pk":apply_inn_instance.pk, "info":apply_inn_instance.info, "phone_num":apply_inn_instance.phone_num, "username":apply_inn_instance.guest.username, "image":apply_inn_instance.guest.image, "address":apply_inn_instance.inn_id.address, "description":apply_inn_instance.inn_id.description, "date":apply_inn_instance.inn_id.date}
            params.append(info)

        return render(request, "matching/applied_inn.html", {"params":params,})
    
def anonymizationCheck(inn_instance):
    if inn_instance.anonymization:
        if "市" in inn_instance.address:
            address = inn_instance.address.split("市")[0]
            address = address + "市"
        elif "郡" in inn_instance.address:
            address = inn_instance.address.split("郡")[0]
            address = address + "郡"
        elif "区" in inn_instance.address:
            address = inn_instance.address.split("区")[0]
            address = address + "区"
        elif "県" in inn_instance.address:
            address = inn_instance.address.split("県")[0]
            address = address + "県"
        elif "道" in inn_instance.address:
            address = inn_instance.address.split("道")[0]
            address = address + "道"
        elif "府" in inn_instance.address:
            address = inn_instance.address.split("府")[0]
            address = address + "府"
        elif "都" in inn_instance.address:
            address = inn_instance.address.split("都")[0]
            address = address + "都"
    else:
        address = inn_instance.address
    return address

class AuthenticatedApply(TemplateView):
    template_name = "matching/auth_apply.html"

    def get(self, request):
        username = request.session.get('username', None)
        user_instance = CustomUser.objects.get(username=username["username"])
        apply_inn_instaces = ApplyInnModel.objects.filter(guest=user_instance, active=True)

        inn_instances = []
        inn_images = []

        for apply_inn_instance in apply_inn_instaces:
            inn_instances.append((apply_inn_instance.inn_id, apply_inn_instance.pk))       

        inn_images_instances = []
        for inn_instance in inn_instances:
            images = InnImageModel.objects.filter(inn_image_id=inn_instance[0])
            inn_images.append(inn_instance[0])
            inn_images.append(inn_instance[1])
            for image in images:
                inn_images.append(image)
            inn_images_instances.append(inn_images)
            inn_images = []

        return render(request, "matching/auth_apply.html", {"instances": inn_images_instances})
    
class Chat(TemplateView):
    template_name="matching/chat.html"

    def get(self, request):
        username = request.session.get('username', None)
        user_instance = CustomUser.objects.get(username=username["username"])
        chat_instance = []

        chat_instances_user1 = ChatModel.objects.filter(user1=user_instance)
        for chat_instance_user1 in chat_instances_user1:
            chat_instance.append(chat_instance_user1)

        chat_instances_user2 = ChatModel.objects.filter(user2=user_instance)
        for chat_instance_user2 in chat_instances_user2:
            chat_instance.append(chat_instance_user2)

        return render(request, "matching/chat.html", {"chats": chat_instance, "user": user_instance})
    
class ChatDetail(TemplateView):
    template_name = "matching/chat_detail.html"
    form_class = SendForm

    def get(self, request):
        param = request.GET.get("param")
        chat_instance = ChatModel.objects.get(chat_id=param)
        chat_content_instance = []
        is_talk = True
        username = request.session.get('username', None)
        user_instance = CustomUser.objects.get(username=username["username"])
        form = self.form_class()

        try:
            chat_contents = ChatContentModel.objects.filter(chat_content_id=chat_instance)
            for chat_content in chat_contents:
                chat_content_instance.append(chat_content)
        except:
            print("トーク内容がありません")
            is_talk = False

        if len(chat_content_instance) == 0:
            is_talk = False

        return render(request, "matching/chat_detail.html", {"is_talk":is_talk, "chat_content_instance":chat_content_instance, "chat_instance":chat_instance, "user":user_instance, "form":form,})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            username = request.session.get('username', None)
            user = CustomUser.objects.get(username=username["username"])
            chat_id = request.POST.get("chat_id")
            chat = ChatModel.objects.get(chat_id=chat_id)
            
            ChatContentModel.objects.create(chat_content_id=chat, contents=content, sender=user)

            custom_url = customUrl(chat.chat_id, "matching:chat")

            return redirect(custom_url)
        
def customUrl(param_value, url_str):
    url = reverse_lazy(url_str)
    custom_url = f"{url}?param={param_value}"

    return custom_url
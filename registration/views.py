from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView, CreateView
from .forms import SignUpForm,LoginForm, UpdateForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import CustomUser
import os
import urllib.parse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from crudinn.models import InnModel, InnImageModel
from matching.models import ApplyInnModel

# Create your views here.
class InitView(TemplateView):
    template_name = "registration/init.html"

class IndexView(TemplateView):
    template_name = "registration/index.html"

    def get(self, request):
        username = request.session.get("username", None)
        inn_instances = []
        inn_images = []
        inn_images_instances = []
        flag = False

        if username is not None:
            user_instance = CustomUser.objects.get(username=username["username"])
            apply_inn_instaces = ApplyInnModel.objects.filter(host=user_instance, active=False,)
            inn_instances = InnModel.objects.filter(username=user_instance)
            for inn_instance in inn_instances:
                images = InnImageModel.objects.filter(inn_image_id=inn_instance)
                inn_images.append(inn_instance)
                for image in images:
                    inn_images.append(image)
                inn_images_instances.append(inn_images)
                inn_images = []
                
        if len(inn_images_instances) == 0:
            flag = True

        return render(request, "registration/index.html", {"instances": inn_images_instances, "apply_inn_instances":apply_inn_instaces, "is_inn":flag,})
            



class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("registration:init")

    def form_valid(self, form):
        instance = form.save(commit=False)
        image_name = form.cleaned_data["image"]

        if image_name.name and not all(ord(c) < 128 for c in image_name.name):
            filename, ext = os.path.splitext(image_name.name)
            encoded_filename = urllib.parse.quote(filename) + ext
            instance.image.name = encoded_filename

        if instance.image:
            img = Image.open(instance.image)
            output_size = (150,150)
            img.thumbnail(output_size)

            img_io = BytesIO()
            img.save(img_io, format=img.format, quality=100)
            img_io.seek(0)

            instance.image = InMemoryUploadedFile(
                img_io, None, f"{instance.image.name.split('.')[0]}.jpg", 'image/jpeg', sys.getsizeof(img_io), None
            )

        instance.save()
        return super().form_valid(form)
    
class LoginView(TemplateView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("registration:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class()
        context['form'] = form
        context['message'] = ''
        return context
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=name, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    request.session['username'] = {'username':name,}
                    return redirect('registration:index')
                else:
                    message="アカウントが有効ではありません。"
                    return render(request, "login.html", {'form': form, 'message':message})
                
            else:
                message="ユーザ名またはパスワードが間違っています。"
                return render(request, "login.html", {'form': form, 'message':message})
        else:
            message="フォームが無効です。"
            return render(request, "login.html", {'form': form, 'message':message})
    
def LogoutView(request):
    logout(request)
    return redirect("registration:init")

class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = UpdateForm
    template_name_suffix = "update"
    success_url = reverse_lazy('registration:index')

    def form_valid(self, form):
        instance = form.save(commit=False)
        image_name = form.cleaned_data["image"]

        if image_name.name and not all(ord(c) < 128 for c in image_name.name):
            filename, ext = os.path.splitext(image_name.name)
            encoded_filename = urllib.parse.quote(filename) + ext
            instance.image.name = encoded_filename

        if instance.image:
            img = Image.open(instance.image)
            output_size = (150,150)
            img.thumbnail(output_size)

            img_io = BytesIO()
            img.save(img_io, format=img.format, quality=100)
            img_io.seek(0)

            instance.image = InMemoryUploadedFile(
                img_io, None, f"{instance.image.name.split('.')[0]}.jpg", 'image/jpeg', sys.getsizeof(img_io), None
            )

        instance.save()
        return super().form_valid(form)
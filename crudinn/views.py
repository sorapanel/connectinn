from typing import Any
from django.shortcuts import render, redirect
from .forms import InnForm, InnUpdateForm
from django.views.generic import TemplateView
import os
import urllib.parse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from .models import InnModel, InnImageModel
from registration.models import CustomUser

# Create your views here.
class RegisterInn(TemplateView):
    template_name = "crudinn/register_inn.html"
    form_class = InnForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            address = form.cleaned_data['address'] 
            description = form.cleaned_data['description']
            date = form.cleaned_data['date']
            images = form.cleaned_data['images']
            anonymization = form.cleaned_data['anonymization']
            username = request.session.get('username', None)

            user_instance = CustomUser.objects.get(username=username['username'])

            inn_instance = InnModel.objects.create(address=address, description=description, username=user_instance, date=date, anonymization=anonymization)

            for image in images:
                if image.name and not all(ord(c) < 128 for c in image.name):
                    filename, ext = os.path.splitext(image.name)
                    encoded_filename = urllib.parse.quote(filename) + ext
                    image.name = encoded_filename

                if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return redirect("registration:index")

                if image:
                    img = Image.open(image)
                    output_size = (150,150)
                    img.thumbnail(output_size)

                    img_io = BytesIO()
                    img.save(img_io, format=img.format, quality=100)
                    img_io.seek(0)

                    image = InMemoryUploadedFile(
                        img_io, None, f"{image.name.split('.')[0]}.jpg", 'image/jpeg', sys.getsizeof(img_io), None
                    )

                    InnImageModel.objects.create(inn_image_id=inn_instance, image=image)

            inn_instance.save()
            return redirect("registration:index")
        return render(request, self.template_name, {'form': form})
    
def deleteInn(request):
    param = request.GET.get("param")
    inn_instance = InnModel.objects.get(inn_id=param)
    inn_images_instances = InnImageModel.objects.filter(inn_image_id=inn_instance)
    for inn_images_instance in inn_images_instances:
        inn_images_instance.delete()
    inn_instance.delete()

    return redirect("registration:index")

def deleteImage(request):
    param = request.GET.get("param")
    inn_images_instance = InnImageModel.objects.get(pk=param)
    inn_images_instances = InnImageModel.objects.filter(inn_image_id=inn_images_instance.inn_image_id)
    if inn_images_instances.count() == 1:
        return redirect("registration:index")
    inn_images_instance.delete()
    return redirect("registration:index")

class UpdateInn(TemplateView):
    template_name = "crudinn/update_inn.html"
    form_class = InnUpdateForm

    def get(self, request):
        param = request.GET.get("param")
        inn_instance = InnModel.objects.get(inn_id=param)
        inn_images_instances = InnImageModel.objects.filter(inn_image_id=inn_instance)
        initial_data = {
            "address":inn_instance.address,
            "description":inn_instance.description,
            "date":inn_instance.date,
        }
        form = self.form_class(initial=initial_data)
        return render(request, "crudinn/update_inn.html", {"form":form, "inn_images_instances":inn_images_instances, "inn_id":param,})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            address = form.cleaned_data['address'] 
            description = form.cleaned_data['description']
            date = form.cleaned_data['date']
            images = form.cleaned_data['images']
            anonymization = form.cleaned_data['anonymization']

            inn_id = request.POST.get("inn_id")

            inn_instance = InnModel.objects.get(inn_id=inn_id)
            
            inn_instance.address = address
            inn_instance.description = description
            inn_instance.date = date
            inn_instance.anonymization = anonymization

            for image in images:
                if image.name and not all(ord(c) < 128 for c in image.name):
                    filename, ext = os.path.splitext(image.name)
                    encoded_filename = urllib.parse.quote(filename) + ext
                    image.name = encoded_filename

                if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return redirect("registration:index")

                if image:
                    img = Image.open(image)
                    output_size = (150,150)
                    img.thumbnail(output_size)

                    img_io = BytesIO()
                    img.save(img_io, format=img.format, quality=100)
                    img_io.seek(0)

                    image = InMemoryUploadedFile(
                        img_io, None, f"{image.name.split('.')[0]}.jpg", 'image/jpeg', sys.getsizeof(img_io), None
                    )

                    InnImageModel.objects.create(inn_image_id=inn_instance, image=image)

            inn_instance.save()
            return redirect("registration:index")

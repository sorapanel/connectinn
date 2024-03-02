from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="ユーザ名", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="パスワード")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="パスワード(再度)")
    first_name = forms.CharField(label="名", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="姓", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="トプ画", required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'image', 'first_name', 'last_name'] 
        labels = {'username':"ユーザ名", 'email':"メールアドレス", 'password1':"パスワード", 'password2':"パスワード（再度）", 'image':"トプ画", 'first_name':"名", 'last_name':"姓"}

class UpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'image', 'first_name', 'last_name'] 
        labels = {'username':"ユーザ名", 'email':"メールアドレス", 'password1':"パスワード", 'image':"トプ画", 'first_name':"名", 'last_name':"姓"}

    username = forms.CharField(label="ユーザ名", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="名", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="姓", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="トプ画", required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    username = forms.CharField(label="ユーザ名", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="パスワード")
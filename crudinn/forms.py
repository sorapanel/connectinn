from django import forms
from django.utils import timezone

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class InnForm(forms.Form):
    address = forms.CharField(label="住所",required=True,)
    anonymization = forms.BooleanField(label="住所を隠す（県名と市名のみ表示）", required=False, initial=False,)
    description = forms.CharField(label="詳細", required=True)
    date = forms.DateField(label="日付", required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min':timezone.localdate(),}))
    images = MultipleFileField(label="写真", required=True)

class InnUpdateForm(forms.Form):
    address = forms.CharField(label="住所",required=True,)
    anonymization = forms.BooleanField(label="住所を隠す（県名と市名のみ表示）", required=False, initial=False,)
    description = forms.CharField(label="詳細", required=True)
    date = forms.DateField(label="日付", required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min':timezone.localdate(),}))
    images = MultipleFileField(label="写真", required=False)
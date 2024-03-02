from django import forms
import re

class CustomPhoneNumField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(self.validate_phone_num)

    def validate_phone_num(self, value):
        if not re.match(r'^\d{3}-\d{4}-\d{4}$', value):
            raise forms.ValidationError('Enter a valid phone number (e.g. 080-0000-0000).')

class ApplyInnForm(forms.Form):
    info = forms.CharField(label="備考", required=True, max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_num = CustomPhoneNumField(label="電話番号（○○○-○○○○-○○○○形式）", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class SendForm(forms.Form):
    content = forms.CharField(label="メッセージ", required=True, max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))

class SearchForm(forms.Form):
    address = forms.CharField(label="住所検索欄", max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))

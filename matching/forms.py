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
    info = forms.CharField(required=True, max_length=500,)
    phone_num = CustomPhoneNumField(required=True,)

class SendForm(forms.Form):
    content = forms.CharField(required=True, max_length=500,)

class SearchForm(forms.Form):
    address = forms.CharField(max_length=500,)

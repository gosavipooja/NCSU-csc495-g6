from django import forms
from django.core.validators import RegexValidator

class ZipcodeForm(forms.Form):
    zipcode = forms.CharField(label='Zipcode', max_length=5, validators=[RegexValidator(regex=r'^\d{5,5}$', message='Has to be a valid US zip code.', code='nomatch')])

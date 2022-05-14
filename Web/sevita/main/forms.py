from django import forms
from .models import *

CHOICES = (
    ("1", '2.5 мл'),
    ("2", '5 мл'),
    ("3", '10 мл')
)


class FeedBack(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="Выберите парфюм", initial=0)
    volume = forms.ChoiceField(choices=CHOICES, label="Выберите объём")
    contacts = forms.EmailField(label='Оставьте e-mail для связи:')
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5, 'placeholder': 'Поле необязательно'}),
        label="Оставьте свои пожелания",
        required=False)

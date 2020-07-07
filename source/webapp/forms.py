from django.forms import ModelForm
from django import forms

from webapp.models import Ad, GROUP_CHOICES, TYPE_CHOICES


class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['number', 'city', 'group', 'description']

class SimpleSearchForm(forms.Form):
    descr = forms.CharField(max_length=100, required=False, label="Текст")
    city = forms.CharField(max_length=100, required=False, label="Город")
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='Тип', required=False)
    group = forms.ChoiceField(choices=GROUP_CHOICES, label='Группа', required=False)

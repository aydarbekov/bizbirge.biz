from django.forms import ModelForm

from webapp.models import Ad


class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['number', 'city', 'group', 'description']
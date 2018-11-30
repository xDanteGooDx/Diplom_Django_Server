from django.contrib.auth.models import User
from django import forms

from MySite.models import Profile


class RegForm(forms.ModelForm):
    patronymic = forms.CharField(label='Отчество', required=False)
    birth = forms.DateField(label='День Рождения')

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', '')

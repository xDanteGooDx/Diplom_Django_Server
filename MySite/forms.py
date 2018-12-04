import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets

from MySite.models import Student


class RegForm(UserCreationForm):
    patronymic = forms.CharField(label='Отчество', required=False, widget=forms.
                                 TextInput(attrs={'class': 'form-control'}))
    birth = forms.DateField(label='День Рождения', required=False,
                            widget=widgets.SelectDateWidget(attrs={'class': 'col-md-3 ml-3 form-control'},
                                                            years=range(1950, datetime.datetime.now().year + 1)))

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'birth', 'email', 'username', 'password1', 'password2')
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['email'].required = True


class StudRegForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('group',)
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudRegForm, self).__init__(*args, **kwargs)
        self.fields['group'].required = True

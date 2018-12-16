import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets

from MySite.models import Student, Profile, Educator, Book


class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'username', 'password1', 'password2')
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
        self.fields['email'].unique = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Такой email уже используется')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('patronymic', 'birth',)
        widgets = {
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'birth': widgets.SelectDateWidget(attrs={'class': 'col-md-3 ml-3 form-control'},
                                              years=range(datetime.datetime.now().year, 1950, -1))
        }

        def __init__(self, *args, **kwargs):
            self.fields['patronymic'].required = False
            self.fields['birth'].required = False


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


class EduRegForm(forms.ModelForm):
    class Meta:
        model = Educator
        fields = ('scientific_degree', 'subject_area')
        widgets = {
            'scientific_degree': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_area': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UploadFileForm(forms.Form):
    file = forms.FileField()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title_book', 'icon_book')
        widgets = {
            'title_book': forms.TextInput(attrs={'class': 'form-control'}),
        }

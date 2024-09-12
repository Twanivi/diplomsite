from django import forms
from .models import *
import re
import string
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    title = forms.CharField(label='Тема письма', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                          'rows': 5}))
    captcha = CaptchaField()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                           'autocomplete': 'off'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'completed_at', 'completed', 'priority', 'user', 'is_favorite']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'user': forms.HiddenInput(),
            'completed_at': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'priority': forms.Select(choices=Tasks.CHOICES_PRIORITY),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        spec_simbols = string.punctuation
        if re.match(r'\d', title):
            raise ValidationError('Заголовок не может начинаться с цифры')
        for i in title:
            if i in spec_simbols:
                raise ValidationError('В заголовке не должно быть спецсимволов')
        return title

    def clean_content(self):
        description = self.cleaned_data['description']
        len_description = len(description)
        if len_description > 600:
            raise ValidationError('Длина поля "description" не должна превышать 600 символов')
        return description


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'completed_at', 'completed', 'priority', 'user', 'is_favorite']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'user': forms.HiddenInput(),
            'completed_at': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'priority': forms.Select(choices=Tasks.CHOICES_PRIORITY),
        }


class AddToFavoriteForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['is_favorite']
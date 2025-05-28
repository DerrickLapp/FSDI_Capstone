from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'type': 'email', 'placeholder': 'Email@email.com'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}))

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from network.models import PostImages


class PostImagesForm(forms.ModelForm):
    
    class Meta:
        model = PostImages
        fields = ('post', "image", 'description')
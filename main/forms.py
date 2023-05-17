from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email','username', 'user_avatar')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email','username', 'user_avatar')

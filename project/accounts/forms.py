from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms

from accounts.models import UserProfile


class UserProfileUpdate(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]


class ProfilePic(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

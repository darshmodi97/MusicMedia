from django import forms
from audio_app.models import Users
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'mobile',)# UserCreationForm class will provide 3 fields default : username,password1, password2

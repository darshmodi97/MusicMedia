from django import forms
from audio_app.models import Users
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class SignUpForm(forms.Form,UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError("Password fields are not matched.")

        return password2
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'mobile',)# UserCreationForm class will provide 3 fields default : username,password1, password2

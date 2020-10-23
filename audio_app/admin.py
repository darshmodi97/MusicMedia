from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from audio_app.models import Songs, Users


# Register your models here.

class SongsAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'movie')
    search_fields = ('name', 'artist', 'movie', 'tags')


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'mobile',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UsersAdmin(admin.ModelAdmin):
    # form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('first_name', 'last_name', 'email', 'mobile','date_joined', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('email', 'mobile', 'first_name', 'last_name')


admin.site.register(Songs, SongsAdmin)
admin.site.register(Users,UsersAdmin)

from django.contrib import admin
from audio_app.models import Songs


# Register your models here.

class SongsAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'movie')
    search_fields = ('name', 'artist', 'movie','tags')


admin.site.register(Songs, SongsAdmin)

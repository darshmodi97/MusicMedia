from django.http import HttpResponse
from django.shortcuts import render
from audio_app.models import Songs
# Create your views here.
def index(request):
    all_songs = Songs.objects.all()
    return  render(request,'index.html',{'songs':all_songs})

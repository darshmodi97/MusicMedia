from django.urls import path
from audio_app import views


urlpatterns=[
    path('',views.index,name='index'),

]
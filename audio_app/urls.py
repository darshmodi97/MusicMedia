from django.urls import path
from audio_app import views


urlpatterns=[
    path('',views.index,name='index'),
    path('signup',views.signup,name='signup'),
    path('login',views.get_login,name='login'),
    path('logout',views.get_logout,name='logout'),
    path('update_profile',views.update_profile,name='update_profile'),
    path('play_song',views.play_song,name='play_song'),
    path('check_email',views.check_email,name='check_email'),
    path('check_mobile',views.check_mobile,name='check_mobile'),
    path('mail_send',views.mail_send,name='mail_send'),
    path('validate_otp',views.validate_otp,name='validate_otp'),
    path('change_password',views.change_password,name='change_password'),
    path('like_dislike',views.like_dislike,name='like_dislike'),
    path('create_playlist',views.create_playlist,name='create_playlist'),
    path('check_song',views.check_song,name='check_song'),
    path('get_playlist',views.get_playlist,name='get_playlist'),


]
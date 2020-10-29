from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
import re
import subprocess
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from audio_app.models import Songs, Users, Playlist, Song_Playlist_mapping, Like_Dislike
from audio_app.forms import SignUpForm
import logging

from audio_app.utils import mail_sending
from django_mp3.settings import STATIC_HOSTNAME

Log_format = "Log Details:  %(levelname)s: %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    format=Log_format)


# Create your views here.

def index(request, get_songs=None, msg=None, msg1=None, new_get_song=None):
    if get_songs:
        return render(request, 'index.html', {'songs': get_songs})
    elif msg and msg1 and new_get_song:
        return render(request, 'index.html', {'msg': msg, 'msg1': msg1, 'songs': new_get_song})
    else:
        all_songs = Songs.objects.all()
        return render(request, 'index.html', {'songs': all_songs})


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        logging.info(f"SignUp form data: {signup_form.data}")
        mobile = signup_form.data['mobile']
        Pattern = re.compile("(0/91)?[7-9][0-9]{9}")

        if mobile.isdigit() == "False" or not Pattern.match(mobile):
            messages.error(request, "please enter valid mobile number ..")
            return redirect('signup')

        elif Users.objects.filter(mobile=signup_form.data['mobile']):
            messages.error(request, "Mobile number is already registered.")
            logging.error("Mobile number is already registered")
            return redirect('signup')

        else:
            if signup_form.is_valid():
                # signup_form.save()
                logging.info(f"SignUp form is saved successfully for {signup_form.data['first_name']} "
                             f"with {signup_form.data['email']}")
                messages.success(request, f"{signup_form.data['first_name']} you have successfully registered..")
                return redirect('login')
            else:
                logging.error(f"Error is : {str(signup_form.errors)}")
                messages.error(request, str(signup_form.errors))
                return redirect('signup')
    else:
        signup_form = SignUpForm()
        logging.info("sent blank signup form..")
        return render(request, 'signup.html', {'form': signup_form})


def get_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        logging.info(f"Authenticating user ")
        if user is not None:
            login(request, user)
            logging.info(f"{user} logged in successfully ")
            messages.success(request, "Login successful..")
            msg = f"Welcome {user.first_name} {user.last_name} to MusicMedia"
            subprocess.Popen(['notify-send', msg])
            return redirect('index')
        else:
            logging.error("User provided Invalid credentials")
            messages.error(request, "Invalid Email or Password..")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def get_logout(request):
    logging.info(f"session of user {request.user.email} is cleared.")
    request.session.clear()
    logout(request)
    logging.info("User logged out successfully.")
    subprocess.Popen(['notify-send', "Logged out successfully."])
    messages.success(request, 'You have successfully logged out..')
    return redirect('index')


def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        print(user.id)
        logging.info(f"url: /update_profile  is called by {user}")
        userdata = Users.objects.get(id=user.id)
        print(userdata)
        if request.method == 'POST':

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')

            userdata.first_name = first_name
            userdata.last_name = last_name
            userdata.email = email
            userdata.mobile = mobile
            userdata.save()
            logging.info(f"Update Profile successfully..for {userdata}")
            subprocess.Popen(['notify-send', "Update Profile successfully.."])
            messages.success(request, 'Your profile is successfully updated.')
            return render(request, 'update_profile.html', {'user': userdata})
        else:

            return render(request, 'update_profile.html', {'user': userdata})
    else:
        messages.error(request, "Sorry! you have to login first.")
        return redirect('login')


def play_song(request):
    song_id = request.GET.get('id')
    song = Songs.objects.get(id=song_id)
    return render(request, "song_page.html", {'song': song})


def change_password(request):
    if request.user.is_authenticated:
        user = request.user
        logging.info(f"url:/change_password is called by {request.user}")
        password = request.POST.get('pass')
        userdata = Users.objects.get(id=user.id)

        userdata.set_password(password)
        userdata.save()
        logging.info(f"Password for {user} is successfully changed .. ")
        subprocess.Popen(['notify-send', "your password is changed sucessfully."])
        return redirect('/')
    else:
        messages.error(request, "You have to login first.")
        return redirect('login')


def check_email(request):
    if request.user.is_authenticated:
        email = request.POST.get('email')
        if email:
            get_email = Users.objects.filter(email=email).first()
            logging.ingo("url: /check_email  checking email whethere it is already registered or not.")
            if get_email:
                return HttpResponse("Email is already exist.")
            else:
                return HttpResponse("Email is available.")
        else:
            return HttpResponse("Email is required.")
    else:
        messages.error(request, "Sorry you have to login first in your account to change your email ")
        return redirect('login')


def check_mobile(request):
    if request.user.is_authenticated:

        mobile = request.POST.get('mobile')
        get_mobile = Users.objects.filter(mobile=mobile).first()
        logging.ingo("url: /check_mobile  checking mobile number whethere it is already registered or not.")
        if get_mobile:
            return HttpResponse("Mobile number is already registered.")
        else:
            return HttpResponse("available")
    else:
        messages.error(request, "Sorry you have to login first in your account to change your mobile number")
        return redirect('login')


def mail_send(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = Users.objects.filter(email=email).first()
        if user:
            otp = str(random.randint(100000, 999999))
            logging.info(f"OTP : {otp} sent to the {user}")
            request.session['otp'] = otp
            subject = "Regarding your password "
            body = f"We are here to Help you, " \
                   f"Here is your One Time Password for the verification : {otp}"
            mail_sending(subject, body, to=[email])

            logging.info(f"Email for verification is sent to the {user}")

            messages.success(request, 'OTP sent to the registered email.')
            return render(request, 'validateOTP.html')
        else:
            messages.error(request, "Oops! Entered email is not registered.")
            return render(request, 'email.html')
    else:
        return render(request, 'email.html')


def validate_otp(request):
    sent_otp = request.session.get('otp')
    received_otp = request.POST.get('otp')
    logging.info("==== validating otp ====")

    if sent_otp == received_otp:
        logging.info("verified successfully..")
        return render(request, 'change_password.html')
    else:
        messages.error(request, "You have entered wrong OTP.")
        return render(request, 'validateOTP.html')


def create_playlist(request):
    if request.user.is_authenticated:
        logging.info(f"url:/create_playlist called by {request.user}")
        user = request.user
        name = request.GET.get('name')
        playlist = Playlist.objects.create(name=name, user_id=user)
        logging.info(f"Playlist created with name {playlist.name} for user {user}")
        return HttpResponse("Playlist created successfully.")
    else:
        messages.error(request, "You have to login first for creating your playlist.")
        return redirect('login')


def check_song(request):
    user = request.user
    song_id = request.GET.get('songid')
    song_data = Like_Dislike.objects.filter(song_id=song_id, user_id=user.id).first()
    logging.info(f"in url: /check_song  song_data :{song_data}")
    if song_data:
        if song_data.status == '1':
            return HttpResponse("song already liked.")
        else:
            return HttpResponse("song is not liked.")
    else:
        return HttpResponse("nothing")


def like_dislike(request):
    if request.user.is_authenticated:
        user = request.user
        song_id = int(request.GET.get('songid'))
        status = request.GET.get('status')
        playlist = Playlist.objects.filter(user_id=user.id).first()
        get_song_id = Songs.objects.filter(id=song_id).first()
        if status == "1":
            if playlist:
                logging.info(f"Playlist {playlist.name} found for the user {user}")
                add_song = Song_Playlist_mapping.objects.create(playlist_id=playlist, song_id=get_song_id)
                logging.info(f"song_id:{add_song.song_id.id} is added to the playlist_id :{add_song.playlist_id.id} ")

                change_status = Like_Dislike.objects.filter(song_id=get_song_id, user_id=user).first()
                if change_status and change_status.status != status:
                    change_status.status = status
                    change_status.save()
                    return HttpResponse("song is added to your playlist.")
                else:
                    like_dislike_song = Like_Dislike.objects.create(song_id=get_song_id, user_id=user, status=status)
                    logging.info(
                        f"{user} Liked the song: {like_dislike_song.song_id.name} song id:{like_dislike_song.song_id.id}  status: {status}")

                    return HttpResponse("song is added to your playlist.")
            else:
                return HttpResponse("You don't have your playlist please create your playlist first.")
        else:
            get_song = Like_Dislike.objects.filter(song_id=get_song_id, user_id=user).first()
            get_song.status = 0
            get_song.save()
            remove_from_playlist = Song_Playlist_mapping.objects.filter(playlist_id=playlist,
                                                                        song_id=get_song.song_id).first()
            remove_from_playlist.delete()
            logging.info(f"{user} Disliked the song: {get_song.song_id} ")
            logging.info(f"song: {song_id} removed from the playlist")
            return HttpResponse("You disliked this song.")
    else:
        return HttpResponse("You have to login into your account to like the songs.")


def get_playlist(request):
    if request.user.is_authenticated:
        user = request.user
        page = request.GET.get('page', 1)
        get_songs_id = Like_Dislike.objects.filter(user_id=user, status=1)
        logging.info(f"{user} Getting playlist ..")
        paginator = Paginator(get_songs_id, 2)  # Show 2 contacts per page.
        try:
            get_songs_id = paginator.page(page)
        except PageNotAnInteger:
            get_songs_id = paginator.page(1)
        except EmptyPage:
            get_songs_id = paginator.page(paginator.num_pages)
        return render(request, 'show_playlist.html', {'songs': get_songs_id})

    else:
        messages.error(request, "You have to login into your account to access the playlist.")
        return redirect('login')


def search_song(request):
    search_data = request.GET.get('search')
    print("search data:", search_data)
    logging.info(f"user searched for {search_data}")
    get_songs = Songs.objects.filter(tags__icontains=search_data)
    print("get_songs:", get_songs)
    logging.info("==== Showing searched songs ====")

    # self made search algorithm with search instead .....
    try:
        if not get_songs:
            s_data = search_data.split(' ')
            for i in s_data:
                get_songs = Songs.objects.filter(tags__icontains=i)
                print("i", i)
                if get_songs:
                    return index(request, get_songs)
                else:
                    break
            l = len(search_data)
            for i in range(l, 0, -1):
                search = search_data[0:i]
                new_get_song = Songs.objects.filter(tags__icontains=search)
                print("search:", search, new_get_song)
                if new_get_song:
                    break
            msg = f"{search_data}"
            msg1 = new_get_song
            temp = None
            return index(request, temp, msg, msg1, new_get_song)
        # temp variable to handle the number of arguments of the index() function...

        else:
            return index(request, get_songs)
    except Exception as e:
        logging.error(f"error {e}")
        return HttpResponse("search result not found.."
                            "<html>"
                            "<body>"
                            "<a href='/'>back</a>"
                            "</body>"
                            "</html>")


def share(request):
    if not request.session.get('s_id'):
        s_id = request.GET.get('id')
        request.session['s_id'] = s_id

    song = Songs.objects.filter(id=request.session.get('s_id')).first()
    print(song)
    logging.info(f"sending link for the song {song.name}")
    song_link = STATIC_HOSTNAME + "/media/" + str(song.song_file)

    if request.method == "POST":
        email = request.POST.get('email')
        subject = "Song Download link"
        body = f"Here is your song : {song_link}"

        mail_sending(subject, body, to=[email])
        logging.info(f"Email for downloading song is sent to the email: {email}")
        messages.success(request, 'Email sent to the user.')
        return redirect('index')

    else:
        return render(request, 'song_share_email.html')

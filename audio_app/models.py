from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime


# custom User Model ..
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, mobile, password=None, commit=True):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))
        if not mobile:
            raise ValueError('Users Must Have an mobile number')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            mobile=mobile,
            last_name=last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, mobile, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email=email,
                                mobile=mobile,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                commit=False, )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Users(AbstractBaseUser):
    # username =None 
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=True, max_length=100)
    mobile = models.CharField(max_length=100, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']
    objects = UserManager()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None
#


class Songs(models.Model):
    name = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    tags = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    song_file = models.FileField(upload_to='files')
    movie = models.CharField(max_length=200, default='album')

    class Meta:
        db_table = 'Songs'
        verbose_name_plural ="Songs"

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=250)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        db_table = "Playlist"

    def __str__(self):
        return self.name


class Song_Playlist_mapping(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song_id = models.ForeignKey(Songs, on_delete=models.CASCADE)

    class Meta:
        db_table = "Song_Playlist_mapping"

    def __str__(self):
        return f"playlist_id {self.playlist_id} and song_id {self.song_id}"


class Like_Dislike(models.Model):
    status_choice = (
        (1, 'Like'),
        (0, 'Dislike')
    )

    song_id = models.ForeignKey(Songs, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    status = models.CharField( max_length=50, choices=status_choice, default=0)

    class Meta:
        db_table = "Like_Dislike"

    def __str__(self):
        return f"song_id {self.song_id} user_id {self.user_id} status {self.status}"

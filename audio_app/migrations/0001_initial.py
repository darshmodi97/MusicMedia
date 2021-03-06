# Generated by Django 3.1.2 on 2021-02-13 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100, unique=True)),
                ('mobile', models.CharField(max_length=100, unique=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Playlist',
            },
        ),
        migrations.CreateModel(
            name='Songs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('artist', models.CharField(max_length=250)),
                ('tags', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images')),
                ('song_file', models.FileField(upload_to='files')),
                ('movie', models.CharField(default='album', max_length=200)),
            ],
            options={
                'db_table': 'Songs',
            },
        ),
        migrations.CreateModel(
            name='Song_Playlist_mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio_app.playlist')),
                ('song_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio_app.songs')),
            ],
            options={
                'db_table': 'Song_Playlist_mapping',
            },
        ),
        migrations.CreateModel(
            name='Like_Dislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(1, 'Like'), (0, 'Dislike')], default=0, max_length=50)),
                ('song_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audio_app.songs')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Like_Dislike',
            },
        ),
    ]

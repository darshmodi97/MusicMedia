# Generated by Django 3.1.2 on 2020-10-20 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_app', '0004_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(blank=True, max_length=100, unique=True),
        ),
    ]

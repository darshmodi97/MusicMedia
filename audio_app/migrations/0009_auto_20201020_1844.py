# Generated by Django 3.1.2 on 2020-10-20 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_app', '0008_auto_20201020_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 20, 18, 44, 20, 495110)),
        ),
    ]

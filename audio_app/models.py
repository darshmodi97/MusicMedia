from django.db import models


# Create your models here.
class Songs(models.Model):
    name = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    tags = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    song_file = models.FileField(upload_to='files')
    movie = models.CharField(max_length=200, default='album')

    class Meta:
        db_table = 'Songs'

    def __str__(self):
        return self.name

from django.db import models

from django.conf.settings import IMAGE_SIZES


class ImageFile(models.Model):
    """Stores an image on a specific location and the dimensions."""
    image = models.FileField()
    height = models.IntegerField()
    width = models.IntegerField()


class Image(models.Model):
    """Stores multiple version of one image in different sizes."""
    files = models.ManyToManyField(ImageFile, related_name='file')

    def save(self, *args, **kwargs):
        if 'image' in kwargs:
            self.process(kwargs.pop('image'))

        super().save(*args, **kwargs)

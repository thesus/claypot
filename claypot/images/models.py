from django.conf import settings
from django.db import models

from claypot.images.utils import delegate

import django_rq
import os.path
import uuid

class ImageFile(models.Model):
    """Stores an image on a specific location and the dimensions."""
    image_file = models.FileField()
    height = models.IntegerField()
    width = models.IntegerField()


class Image(models.Model):
    """Stores multiple version of one image in different sizes."""
    files = models.ManyToManyField(ImageFile)

    def save(self, *args, **kwargs):
        image = kwargs.pop('image', None)
        super().save(*args, **kwargs)
        if image:
            self.process(image)

    def process(self, image):
        name = "{0}.{1}".format(
            uuid.uuid4(),
            image.name.split(".")[-1]
        )
        fullpath = os.path.join(settings.IMAGE_ROOT, name)
        with open(fullpath, 'wb') as f:
            for c in image.chunks():
                f.write(c)

        queue = django_rq.get_queue('default')
        queue.enqueue(
            delegate,
            classes=(Image, ImageFile),
            pk=self.pk,
            filename=name
        )

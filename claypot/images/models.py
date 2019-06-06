import errno
import os
import uuid

from django.conf import settings
from django.db import models
import django_rq


class ImageFile(models.Model):
    """Stores an image on a specific location and the dimensions."""

    image_file = models.FileField()
    height = models.IntegerField()
    width = models.IntegerField()


class Image(models.Model):
    """Stores multiple version of one image in different sizes."""

    files = models.ManyToManyField(ImageFile)

    thumbnail = models.ForeignKey(
        ImageFile,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="parent",
    )

    def save(self, *args, **kwargs):
        image = kwargs.pop("image", None)
        super().save(*args, **kwargs)
        if image:
            self.process(image)

    def process(self, image):
        name = "{0}.{1}".format(uuid.uuid4(), image.name.split(".")[-1])

        try:
            os.makedirs(settings.IMAGE_ROOT)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        fullpath = os.path.join(settings.IMAGE_ROOT, name)
        with open(fullpath, "wb") as f:
            for c in image.chunks():
                f.write(c)

        queue = django_rq.get_queue("default")
        queue.enqueue("claypot.images.utils.delegate", pk=self.pk, filename=name)

import os.path
from io import BytesIO

import django_rq
import PIL.Image
import PIL.ImageOps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile

from .models import Image, ImageFile


def resize(pk, filename, name, dimensions):
    fullpath = os.path.join(settings.IMAGE_ROOT, filename)
    image = PIL.Image.open(fullpath)

    orig_width, orig_height = image.size

    # Could look like this: 'small': { 'w': 300 }
    fit = False
    if ("w" in dimensions) and ("h" in dimensions):
        h = dimensions["h"]
        w = dimensions["w"]
        fit = True
    elif "w" in dimensions:
        w = dimensions["w"]
        h = (float(w) / orig_width) * orig_height
    elif "h" in dimensions:
        h = dimensions["h"]
        w = (float(h) / orig_height) * orig_width
    else:
        raise ImproperlyConfigured("Image settings contain wrong keys!")

    h = int(h)
    w = int(w)

    with BytesIO() as f:
        instance = ImageFile()
        instance.height = h
        instance.width = w

        if fit:
            image = PIL.ImageOps.fit(
                image=image, method=PIL.Image.LANCZOS, size=(w, h), centering=(0.5, 0.5)
            )
        else:
            image = image.resize((w, h), PIL.Image.LANCZOS)

        # Convert to remove possible alpha channel
        image = image.convert("RGB")
        image.save(f, format="jpeg")

        instance.image_file.save(
            "{0}_{1}.jpg".format(pk, name), ContentFile(f.getvalue()), save=False
        )

        instance.save()
        return instance


def delegate(pk, filename):
    image = Image.objects.get(pk=pk)

    for (k, v) in settings.IMAGE_SIZES.items():
        image.files.add(resize(pk, filename, k, v))

    image.thumbnail = resize(pk, filename, "thumbnail", settings.THUMBNAIL_SIZE)
    image.save()

from io import BytesIO
import os.path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
import PIL.Image
import PIL.ImageOps
import django_rq


def resize(pk, filename, name, dimensions, image_class, file_class):
    container = image_class.objects.get(pk=pk)

    fullpath = os.path.join(settings.IMAGE_ROOT, filename)
    image = PIL.Image.open(fullpath)

    orig_width, orig_height = image.size

    # Could look like this: 'small': { 'w': 300 }
    fit = False
    if ('w' in dimensions) and ('h' in dimensions):
        h = dimensions['h']
        w = dimensions['w']
        fit = True
    elif ('w' in dimensions):
        w = dimensions['w']
        h = (float(w) / orig_width) * orig_height
    elif ('h' in dimensions):
        h = dimensions['h']
        w = (float(h) / orig_height) * orig_width
    else:
        raise ImproperlyConfigured("IMAGE_SIZES contains wrong keys")

    h = int(h)
    w = int(w)

    with BytesIO() as f:
        instance = file_class()
        instance.height = h
        instance.width = w

        if fit:
            image = PIL.ImageOps.fit(
                image=image,
                method=PIL.Image.LANCZOS,
                size=(w, h),
                centering=(0.5, 0.5),
            )
        else:
            image = image.resize(
                (w, h),
                PIL.Image.LANCZOS,
            )

        # Convert to remove possible alpha channel
        image = image.convert("RGB")
        image.save(f, format='jpeg')

        instance.image_file.save(
            '{0}_{1}.jpg'.format(container.pk, name),
            ContentFile(f.getvalue()),
            save=False,
        )

        instance.save()
        container.files.add(instance)


def delegate(classes, pk, filename):
    for (k, v) in settings.IMAGE_SIZES.items():
        resize(pk, filename, k, v, classes[0], classes[1])

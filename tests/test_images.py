from io import BytesIO

import django_rq

import PIL.Image
import pytest
from django.conf import settings
from django.core.files.base import File
from django.urls import reverse
from fakeredis import FakeStrictRedis
from rq import Queue

from claypot.images.models import Image


@pytest.fixture
def uploaded_image(api_client, user, monkeypatch):
    api_client.force_login(user)

    queue = Queue(is_async=False, connection=FakeStrictRedis())

    def mockreturn(name):
        return queue

    monkeypatch.setattr(django_rq, "get_queue", mockreturn)

    size = (1200, 1000)
    f = BytesIO()

    image = PIL.Image.new("RGBA", size=size, color=(256, 0, 0))
    image.save(f, "png")
    f.seek(0)

    return {
        "size": size,
        "response": api_client.post(
            reverse("api:image-list"),
            {"image": File(f, "image.png")},
            format="multipart",
        ),
    }


@pytest.mark.django_db
def test_image_upload(uploaded_image):
    assert uploaded_image["response"].status_code == 200


@pytest.mark.django_db
def test_image_formats(uploaded_image):
    # '{'thumbnail': {'w': 200, 'h': 200}, 'small': {'w': 400}, 'medium': {'w': 700}, 'large': {'w': 1000}'
    instance = Image.objects.get(pk=uploaded_image["response"].data["id"])
    files = instance.files.all()

    # For every size in settings there should be an image.
    assert len(settings.IMAGE_SIZES) == files.count()

    uploaded_ratio = float(uploaded_image["size"][0]) / uploaded_image["size"][1]
    for v in settings.IMAGE_SIZES.values():
        k = v.keys()
        if "w" in k and "h" in k:
            assert files.filter(width=v["w"], height=v["h"]).exists()
        else:
            image_file = None
            if "w" in k:
                image_file = files.filter(
                    width=v["w"]
                ).first()  # We should check that there's only one....
                print(image_file)
            elif "h" in k:
                image_file = files.filter(height=v["h"]).first()

            assert image_file is not None

            size = PIL.Image.open(image_file.image_file.path).size

            assert image_file.width == size[0]
            assert image_file.height == size[1]

            ratio = image_file.width / image_file.height

            assert pytest.approx(uploaded_ratio, 0.01) == ratio

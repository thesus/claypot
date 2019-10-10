from .models import Image, ImageFile

from rest_framework import serializers


class ImageCreateSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = ["image_file", "height", "width"]
        read_only_fields = ["image_file", "height", "width"]


class ImageRetrieveSerializer(serializers.ModelSerializer):
    files = ImageFileSerializer(many=True)
    thumbnail = ImageFileSerializer()

    class Meta:
        model = Image
        fields = ["id", "files", "thumbnail"]
        read_only_fields = ["id", "files"]


class ImageThumbnailSerializer(serializers.ModelSerializer):
    thumbnail = ImageFileSerializer()

    class Meta:
        model = Image
        fields = ["thumbnail"]
        read_only_fields = ["thumbnail"]

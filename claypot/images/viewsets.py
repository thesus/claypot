from .models import Image
from .serializers import ImageCreateSerializer, ImageRetrieveSerializer

from claypot.api.permissions import ReadAllEditOwn

from rest_framework import viewsets
from rest_framework.response import Response


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = [ReadAllEditOwn]

    def get_serializer_class(self):
        if self.action == "create":
            return ImageCreateSerializer
        else:
            return ImageRetrieveSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Image()
        instance.save(**serializer.validated_data)

        return Response({"id": instance.pk})

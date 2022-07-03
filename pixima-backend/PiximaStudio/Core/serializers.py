from rest_framework.serializers import Serializer
from . import models


class UploadImageSerializer(Serializer):
    class Meta:
        model = models.UploadImageModel
        fields = ['Image']

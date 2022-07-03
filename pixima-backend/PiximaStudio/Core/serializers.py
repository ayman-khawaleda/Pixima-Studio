from rest_framework.serializers import ModelSerializer
from . import models


class UploadImageSerializer(ModelSerializer):
    class Meta:
        model = models.UploadImageModel
        fields = ['Image']

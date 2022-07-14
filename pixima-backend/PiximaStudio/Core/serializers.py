from operator import mod
from pyexpat import model
from rest_framework.serializers import ModelSerializer, Serializer, UUIDField
from . import models


class UploadImageSerializer(ModelSerializer):
    class Meta:
        model = models.ImageModel
        fields = ["Image"]


class GetImageSerializer(Serializer):
    id = UUIDField(format="hex_verbose")

    def create(self, validated_data):
        return models.ImageModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.save()
        return instance

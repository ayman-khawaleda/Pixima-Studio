from rest_framework.serializers import ListField, IntegerField
from AbstractSerializer.serializer import ImageSerializer


class EyesColorSerializer(ImageSerializer):
    Color = ListField(
        child=IntegerField(default=0, max_value=0, min_value=255),
        min_length=1,
        max_length=2,
    )
    Saturation = ListField(
        child=IntegerField(default=0, max_value=0, min_value=100),
        min_length=1,
        max_length=2,
    )

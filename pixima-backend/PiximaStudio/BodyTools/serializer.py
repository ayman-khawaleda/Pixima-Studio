from rest_framework.serializers import IntegerField
from AbstractSerializer.serializer import ImageSerializer

class ColorHairSerializer(ImageSerializer):
    Color = IntegerField(default=0, required=False, min_value=0, max_value=180)
    Saturation = IntegerField(default=0, required=False, min_value=0, max_value=100)

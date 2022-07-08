from rest_framework.serializers import IntegerField
from AbstractSerializer.serializer import ImageSerializer


class GlitchFilterSerializer(ImageSerializer):
    Shift = IntegerField(default=20, required=False)
    Step = IntegerField(default=15, required=False)
    Density = IntegerField(default=5, required=False)
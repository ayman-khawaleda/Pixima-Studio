from rest_framework.serializers import IntegerField,CharField
from AbstractSerializer.serializer import ImageSerializer


class GlitchFilterSerializer(ImageSerializer):
    Shift = IntegerField(default=20, required=False)
    Step = IntegerField(default=15, required=False)
    Density = IntegerField(default=5, required=False)

class CirclesFilterSerializer(ImageSerializer):
    X = IntegerField(default=-1, required=False)
    Y = IntegerField(default=-1, required=False)
    FaceKey = CharField(default="None",required=False)
    Radius = IntegerField(default=15,required=False)
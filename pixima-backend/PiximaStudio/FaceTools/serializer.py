from rest_framework.serializers import ListField, IntegerField, FloatField, CharField
from AbstractSerializer.serializer import ImageSerializer


class EyesColorSerializer(ImageSerializer):
    Color = ListField(
        child=IntegerField(default=0, min_value=0, max_value=255),
        min_length=1,
        max_length=2,
    )
    Saturation = ListField(
        child=IntegerField(default=0, min_value=0, max_value=100),
        min_length=1,
        max_length=2,
    )


class EyesResizeSerializer(ImageSerializer):
    Factor = FloatField(default=1.1, required=False, min_value=0.75, max_value=2)
    Radius = IntegerField(default=75, required=False, min_value=50, max_value=200)


class NoseResizeSerializer(ImageSerializer):
    X = IntegerField(default=0, required=False, min_value=-50, max_value=50)
    Y = IntegerField(default=0, required=False, min_value=-50, max_value=50)
    Factor = FloatField(default=1.1, required=False, min_value=0.75, max_value=2)
    Radius = IntegerField(default=75, required=False, min_value=50, max_value=200)


class SmoothFaceSeializer(ImageSerializer):
    Method = CharField(default="BiB", required=False)
    Kernal = IntegerField(default=5, required=False, min_value=3, max_value=31)
    SigmaX = IntegerField(default=0, required=False, min_value=0, max_value=150)
    SigmaY = IntegerField(default=0, required=False, min_value=0, max_value=150)


class WhiteTeethToolSerializer(ImageSerializer):
    Saturation = IntegerField(default=40, required=False, min_value=0, max_value=255)
    Brightness = IntegerField(default=20, required=False, min_value=0, max_value=255)


class ColorLipsToolSerializer(ImageSerializer):
    Color = IntegerField(default=0, required=False, min_value=0, max_value=180)
    Saturation = IntegerField(default=0, required=False, min_value=0, max_value=100)

class SmileToolSerializer(ImageSerializer):
    Factor = IntegerField(default=5, required=False, min_value=-50, max_value=50)
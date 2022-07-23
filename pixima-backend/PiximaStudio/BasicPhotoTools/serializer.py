from rest_framework.serializers import (
    CharField,
    IntegerField,
    BooleanField,
)
from AbstractSerializer.serializer import ImageSerializer

class CropImageSerializer(ImageSerializer):
    X1 = IntegerField(default=-1, required=False, allow_null=True)
    X2 = IntegerField(default=-1, required=False, allow_null=True)
    Y1 = IntegerField(default=-1, required=False, allow_null=True)
    Y2 = IntegerField(default=-1, required=False, allow_null=True)
    Ratio = CharField(default="", required=False, allow_null=True)


class FlipImageSerializer(ImageSerializer):
    Direction = CharField(default="Hor", required=False, allow_null=True)


class RotateImageSerializer(ImageSerializer):
    Angle = IntegerField(default=90, required=False, allow_null=True)
    ClockWise = BooleanField(default=True, required=False, allow_null=True)
    AreaMode = CharField(default="constant", required=False, allow_null=True)


class ResizeImageSerializer(ImageSerializer):
    Width = IntegerField(default=720, required=False, allow_null=True)
    High = IntegerField(default=480, required=False, allow_null=True)


class ContrastImageSerializer(ImageSerializer):
    Contrast = IntegerField(default=50, required=False, allow_null=True)
    Brightness = IntegerField(default=0, required=False, allow_null=True)


class SaturationImageSerializer(ImageSerializer):
    Saturation = IntegerField(default=0, required=False, allow_null=True)

class ChangeColorToolSerializer(ImageSerializer):
    X = IntegerField(required=True,min_value=0)
    Y = IntegerField(required=True,min_value=0)
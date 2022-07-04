from rest_framework.serializers import Serializer,UUIDField,ImageField,CharField,IntegerField,BooleanField


class ImageHandlerSerializer(Serializer):
    id = UUIDField(default='',required=False,allow_null=True,format='hex_verbose')
    Image = ImageField(default='',required=False,allow_null=True)
    Preview = CharField(default='None',required=False)

class CropImageSerializer(ImageHandlerSerializer):
    X1 = IntegerField(default=-1,required=False,allow_null=True)
    X2 = IntegerField(default=-1,required=False,allow_null=True)
    Y1 = IntegerField(default=-1,required=False,allow_null=True)
    Y2 = IntegerField(default=-1,required=False,allow_null=True)
    Ratio = CharField(defualt='1:1',required=False,allow_null=True)


class FlipImageSerializer(ImageHandlerSerializer):
    Direction = CharField(defualt='Hor',required=False,allow_null=True)

class RotateImageSerializer(ImageHandlerSerializer):
    Angle = IntegerField(default=90,required=False,allow_null=True)
    ClockWise = BooleanField(default=True,required=False,allow_null=True)

class ResizeImageSerializer(ImageHandlerSerializer):
    Width = IntegerField(default=720,required=False,allow_null=True)
    High = IntegerField(default=-480,required=False,allow_null=True)


class ContrastImageSerializer(ImageHandlerSerializer):
    Contrast = IntegerField(default=1,required=False,allow_null=True)
    Brightness = IntegerField(default=0,required=False,allow_null=True)

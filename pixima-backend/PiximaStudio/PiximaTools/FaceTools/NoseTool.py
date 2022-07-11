from rest_framework.serializers import IntegerField, FloatField, Serializer
from .FaceTools import FaceTool
from PiximaTools.AI_Models import face_detection_model
from PiximaTools.Exceptions import RequiredValue


class NoseResizeTool(FaceTool):
    def __init__(self, faceDetector=None):
        if faceDetector is None:
            faceDetector = face_detection_model
        self.faceDetector = faceDetector

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def save_mask(self, *args, **kwargs):
        raise Exception("Not Implemented")

    def add_factor(self, factor=1.1, serializer=None):
        if serializer:
            factor = serializer.data["Factor"]
        elif type(factor.dict()) == dict:

            class FactorSerializer(Serializer):
                Factor = FloatField(
                    default=1.1, required=False, min_value=0.75, max_value=2
                )

            factor_serializer = FactorSerializer(data=factor)
            if not factor_serializer.is_valid():
                raise RequiredValue("Invalid Factor Value")
            factor = factor_serializer.data["Factor"]
        else:
            raise RequiredValue("Factor Range [0.75, 2]")

        self.factor = factor
        return self

    def add_radius(self, radius=75, serializer=None):
        if serializer:
            radius = serializer.data["Radius"]
        elif type(radius.dict()) == dict:

            class RadiusSerializer(Serializer):
                Radius = IntegerField(
                    default=75, required=False, min_value=50, max_value=200
                )

            radius_serializer = RadiusSerializer(data=radius)
            if not radius_serializer.is_valid():
                raise RequiredValue("Invalid Radius Value")
            radius = radius_serializer.data["Radius"]
        else:
            raise RequiredValue("Factor Range [50, 200]")
        self.radius = radius
        return self

    def add_x(self, x=0, serializer=None):
        if serializer:
            x = serializer.data["X"]
        elif type(x.dict()) == dict:

            class XSerializer(Serializer):
                X = IntegerField(default=0, required=False, min_value=-50, max_value=50)

            x_serializer = XSerializer(data=x)
            if not x_serializer.is_valid():
                raise RequiredValue("Invalid X Value")
            x = x_serializer.data["X"]
        else:
            raise RequiredValue("X Range [-50, 50]")
        self.x = x
        return self

    def add_y(self, y=0, serializer=None):
        if serializer:
            y = serializer.data["Y"]
        elif type(y.dict()) == dict:

            class YSerializer(Serializer):
                Y = IntegerField(default=0, required=False, min_value=-50, max_value=50)

            y_serializer = YSerializer(data=y)
            if not y_serializer.is_valid():
                raise RequiredValue("Invalid Y Value")
            y = y_serializer.data["Y"]
        else:
            raise RequiredValue("Y Range [-50, 50]")
        self.y = y
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_factor(request.data)
            .add_radius(request.data)
            .add_x(request.data)
            .add_y(request.data)
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_factor(serializer=serializer)
            .add_radius(serializer=serializer)
            .add_x(serializer=serializer)
            .add_y(serializer=serializer)
        )

    def apply(self, *args, **kwargs):
        return self

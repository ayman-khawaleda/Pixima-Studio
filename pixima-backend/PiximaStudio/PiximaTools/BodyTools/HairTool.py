from rest_framework.serializers import Serializer,IntegerField
from PiximaTools.abstractTools import BodyTool
from PiximaTools.AI_Models import face_detection_model,HairSegmentationModel
from PiximaTools.Exceptions import NoFace,RequiredValue
import cv2

class ColorHairTool(BodyTool):
    def __init__(self, faceDetector=None,hair_seg_model = None, saturation=0, color=0) -> None:
        if faceDetector is None:
            faceDetector = face_detection_model
        if hair_seg_model is None:
            hair_seg_model = HairSegmentationModel()
        self.model = hair_seg_model
        self.faceDetector = faceDetector
        self.saturation = saturation
        self.color = color

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_saturation(self, saturation=0, serialzier=None):
        if serialzier:
            saturation = serialzier.data["Saturation"]
        elif type(saturation.dict()) == dict:

            class SaturationSerializer(Serializer):
                Saturation = IntegerField(
                    default=0, required=False, min_value=0, max_value=100
                )

            saturation_serializer = SaturationSerializer(data=saturation)
            if not saturation_serializer.is_valid():
                raise RequiredValue("Saturation Value Is Invalid")
            saturation = saturation_serializer.data["Saturation"]
        self.saturation = saturation
        return self

    def add_color(self, color=0, serialzier=None):
        if serialzier:
            color = serialzier.data["Color"]
        elif type(color.dict()) == dict:

            class ColorSerializer(Serializer):
                Color = IntegerField(
                    default=0, required=False, min_value=0, max_value=180
                )

            color_serializer = ColorSerializer(data=color)
            if not color_serializer.is_valid():
                raise RequiredValue("Color Value Is Invalid")
            color = color_serializer.data["Color"]
        self.color = color
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_saturation(request.data)
            .add_color(request.data)
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_saturation(serialzier=serializer)
            .add_color(serialzier=serializer)
        )

import time
from rest_framework.serializers import Serializer, IntegerField
from PiximaTools.abstractTools import BodyTool
from PiximaTools.AI_Models import (
    face_detection_model,
    HairSegmentationModel,
    selfie_segmentation_model,
)
from PiximaTools.Exceptions import NoFace, RequiredValue
from skimage.color import rgb2gray
import cv2
import numpy as np


class ColorHairTool(BodyTool):
    def __init__(
        self,
        faceDetector=None,
        selfie_segmentation=None,
        hair_seg_model=None,
        saturation=0,
        color=0,
        IMH=256,
        IMW=256
    ) -> None:
        if faceDetector is None:
            faceDetector = face_detection_model
        if hair_seg_model is None:
            hair_seg_model = HairSegmentationModel()
        if selfie_segmentation is None:
            selfie_segmentation = selfie_segmentation_model
        self.selfieSegmentation = selfie_segmentation
        self.hair_segmentation = hair_seg_model
        self.faceDetector = faceDetector
        self.saturation = saturation
        self.color = color
        self.__IMH = IMH
        self.__IMW = IMW

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

    def __selfie_mask(self):
        BG_COLOR = (192, 192, 192) 
        MASK_COLOR = (255, 255, 255)
        image = self.Image
        results = self.selfieSegmentation.process(image)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        fg_image = np.zeros(image.shape, dtype=np.uint8)
        fg_image[:] = MASK_COLOR
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        mask = np.where(condition, fg_image, bg_image)
        newImage = np.ones_like(mask) * 255
        cond = mask == 255
        newImage[cond] = self.Image[cond]
        self.InputImage = newImage
        
    def __model_mask(self):
        h, w, _ = self.InputImage.shape
        model_input_img = cv2.resize(
            rgb2gray(self.InputImage),
            (self.__IMH, self.__IMW),
            interpolation=cv2.INTER_CUBIC,
        ).reshape((self.__IMH, self.__IMW, 1))
        model_mask = self.hair_segmentation.predict(model_input_img)
        model_mask = cv2.normalize(model_mask, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        model_mask = cv2.threshold(
            model_mask.reshape((self.__IMH, self.__IMW, 1)),
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]
        mask = np.zeros(model_mask.shape)
        contours, hierarchy = cv2.findContours(model_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        tup = [[cv2.contourArea(c),c] for c in contours]
        tup.sort(key=lambda x:x[0],reverse=True)
        mask = cv2.drawContours(mask,[tup[0][1]],-1,(255,255,255),-1)
        self.model_mask = cv2.resize(mask,(w,h),interpolation=cv2.INTER_CUBIC)

    def __color_hair(self):
        hsv_image = cv2.cvtColor(self.Image,cv2.COLOR_RGB2HSV)
        h,s,v = cv2.split(hsv_image)
        mask = cv2.GaussianBlur(self.model_mask,(3,3),0.5)
        mask = cv2.morphologyEx(mask,cv2.MORPH_ERODE,(15,35),iterations=10)
        mask = np.roll(mask,-5,0)
        cond = mask >= 1
        h[cond] = self.color
        s[cond] += self.saturation
        hsv_image = cv2.merge([h,s,v])
        self.Image = cv2.cvtColor(hsv_image,cv2.COLOR_HSV2RGB)

    def apply(self, *args, **kwargs):
        self.__selfie_mask()
        self.__model_mask()
        self.__color_hair()
        self.Mask = self.model_mask
        return self

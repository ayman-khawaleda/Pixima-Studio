from abc import abstractmethod, ABC

from requests import request
from PiximaTools.abstractTools import Tool
from PiximaStudio.settings import MEDIA_ROOT, MEDIA_URL
from skimage import io
from PiximaTools.Exceptions import ImageNotSaved, RequiredValue, NoFace
from PiximaTools.AI_Models import face_mesh_model
from rest_framework.serializers import CharField, IntegerField, Serializer
import os
import numpy as np
import cv2


class FaceTool(Tool, ABC):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

    def save_mask(self, *args, **kwargs):
        try:
            sub_path = os.path.join(MEDIA_ROOT, "ImageMasks", str(self.directory_id))
            if not os.path.exists(sub_path):
                os.mkdir(sub_path)
            self.lastidx = len(os.listdir(sub_path))
            full_path = os.path.join(sub_path, f"{self.lastidx}.jpg")
            cv2.imwrite(full_path, self.Mask)
            mask_path = os.path.join(
                MEDIA_URL, "ImageMasks", str(self.directory_id), f"{self.lastidx}.jpg"
            )
            return mask_path
        except Exception as e:
            raise ImageNotSaved("Error In Save Image Mask")


class SmoothFaceTool(FaceTool):
    def __init__(self, faceMeshDetector=None, method_options=["BiB", "GaB"]):
        if faceMeshDetector is None:
            faceMeshDetector = face_mesh_model
        self.faceMeshDetector = faceMeshDetector
        self.method_options = method_options

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_method(self, method="BiB", serializer=None):
        if serializer:
            method = serializer.data["Method"]
        elif type(method) == str and not method in self.method_options:
            method = "BiB"
        elif type(method.dict()) == dict:
            temp_method = method.get("Method", "BiB")
            if temp_method in self.method_options:
                method = temp_method
        else:
            raise RequiredValue("Valid Method Values ['BiB', 'GaB']")
        self.method = method
        return self

    def add_kernal(self, kernal=5, serialzier=None):
        if serialzier:
            kernal = serialzier.data["Method"]
        elif type(kernal.dict()) == dict:

            class KernalSerializer(Serializer):
                Kernal = IntegerField(
                    default=5, required=False, min_value=3, max_value=31
                )

            kernal_serializer = KernalSerializer(data=request.data)
            if not kernal_serializer.is_valid():
                raise RequiredValue(**kernal_serializer.errors)
            kernal = kernal_serializer.data["Kernal"]
        self.kernal = kernal
        return self

    def add_sigmax(self, kernal=5, serialzier=None):
        if serialzier:
            kernal = serialzier.data["Method"]
        elif type(kernal.dict()) == dict:

            class KernalSerializer(Serializer):
                Kernal = IntegerField(
                    default=5, required=False, min_value=3, max_value=31
                )

            kernal_serializer = KernalSerializer(data=request.data)
            if not kernal_serializer.is_valid():
                raise RequiredValue(**kernal_serializer.errors)
            kernal = kernal_serializer.data["Kernal"]
        self.kernal = kernal
        return self

    def add_sigmax(self, sigmax=5, serialzier=None):
        if serialzier:
            sigmax = serialzier.data["SigmaX"]
        elif type(sigmax.dict()) == dict:

            class SigmaXSerializer(Serializer):
                SigmaX = IntegerField(
                    default=0, required=False, min_value=0, max_value=150
                )

            sigmax_serializer = SigmaXSerializer(data=request.data)
            if not sigmax_serializer.is_valid():
                raise RequiredValue(**sigmax_serializer.errors)
            sigmax = sigmax_serializer.data["SigmaX"]
        self.sigmax = sigmax
        return self

    def add_sigmay(self, sigmay=5, serialzier=None):
        if serialzier:
            sigmay = serialzier.data["SigmaY"]
        elif type(sigmay.dict()) == dict:

            class SigmaYSerializer(Serializer):
                SigmaY = IntegerField(
                    default=0, required=False, min_value=0, max_value=150
                )

            sigmay_serializer = SigmaYSerializer(data=request.data)
            if not sigmay_serializer.is_valid():
                raise RequiredValue(**sigmay_serializer.errors)
            sigmay = sigmay_serializer.data["SigmaY"]
        self.sigmay = sigmay
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_method(request)
            .add_kernal(request)
            .add_sigmax(request)
            .add_sigmay(request)
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_method(serializer=serializer)
            .add_kernal(serialzier=serializer)
            .add_sigmax(serialzier=serializer)
            .add_sigmay(serialzier=serializer)
        )

    def apply(self, *args, **kwargs):
        return self

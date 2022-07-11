from abc import abstractmethod, ABC
from PiximaTools.abstractTools import Tool
from PiximaStudio.settings import MEDIA_ROOT, MEDIA_URL
from skimage import io
from PiximaTools.Exceptions import ImageNotSaved,RequiredValue,NoFace
from PiximaTools.AI_Models import face_mesh_model
from rest_framework.serializers import CharField,IntegerField,Serializer
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
            cv2.imwrite(full_path,self.Mask)
            mask_path = os.path.join(
                MEDIA_URL, "ImageMasks", str(self.directory_id), f"{self.lastidx}.jpg"
            )
            return mask_path
        except Exception as e:
            raise ImageNotSaved("Error In Save Image Mask")

class SmoothFaceTool(FaceTool):
    
    def __init__(self, faceMeshDetector=None):
        if faceMeshDetector is None:
            faceMeshDetector = face_mesh_model
        self.faceMeshDetector = faceMeshDetector

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def request2data(self, request):
        return (
            super()
            .request2data(request)
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
        )

    def apply(self,*args,**kwargs):
        return self
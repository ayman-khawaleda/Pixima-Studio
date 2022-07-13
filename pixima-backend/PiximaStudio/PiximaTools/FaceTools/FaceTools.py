from abc import abstractmethod, ABC

from requests import request
from PiximaTools.abstractTools import Tool
from PiximaStudio.settings import MEDIA_ROOT, MEDIA_URL
from skimage import io
from skimage.color import rgb2gray
from PiximaTools.Exceptions import ImageNotSaved, RequiredValue, NoFace
from PiximaTools.AI_Models import (
    DNNModel,
    face_mesh_model,
    mp_drawing_styles,
    face_detection_model,
    DrawingSpec,
    draw_landmarks,
)
from rest_framework.serializers import CharField, IntegerField, Serializer
import os
import numpy as np
import cv2


class FaceLandMarksArray:
    lips_upper = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
    lips_lower = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]
    rightEyeUpper = [246, 161, 160, 159, 158, 157, 173]
    rightEyeLower = [33, 7, 163, 144, 145, 153, 154, 155, 133]
    leftEyeUpper = [466, 388, 387, 386, 385, 384, 398]
    leftEyeLower = [263, 249, 390, 373, 374, 380, 381, 382, 362]
    rightEyeBrowUpper = [156, 70, 63, 105, 66, 107, 55]
    rightEyeBrowLower = [65, 52, 53, 46]
    leftEyeBrowUpper = [383, 300, 293, 334, 296, 336, 285]
    leftEyeBrowLower = [295, 282, 283, 276]
    lipsUpperOuter = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
    lipsLowerOuter = [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
    faceOval = mp_drawing_styles.face_mesh_connections.FACEMESH_FACE_OVAL


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
    def __init__(
        self,
        faceDetector=None,
        faceMeshDetector=None,
        face_segmentation=None,
        imh=256,
        imw=256,
        method_options=["BiB", "GaB"],
    ):
        if faceMeshDetector is None:
            faceMeshDetector = face_mesh_model
        if faceDetector is None:
            faceDetector = face_detection_model
        if face_segmentation is None:
            face_segmentation = DNNModel()

        self.faceMeshDetector = faceMeshDetector
        self.method_options = method_options
        self.face_segmentation = face_segmentation
        self.__IMH, self.__IMW = imh, imw

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

    def __maskEyes(self, face_landmarks):
        h, w, _ = self.faceImage.shape
        pointsRightEye = []
        pointsLeftEye = []
        eyes_mask = np.zeros((h, w))
        for i in FaceLandMarksArray.rightEyeUpper:
            xru, yru = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xru, yru = self.normaliz_pixel(xru, yru, w, h)
            pointsRightEye.append((xru, yru))
        for i in FaceLandMarksArray.rightEyeLower:
            xrl, yrl = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xrl, yrl = self.normaliz_pixel(xrl, yrl, w, h)
            pointsRightEye.append((xrl, yrl))
        for i in FaceLandMarksArray.leftEyeUpper:
            xlu, ylu = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xlu, ylu = self.normaliz_pixel(xlu, ylu, w, h)
            pointsLeftEye.append((xlu, ylu))
        for i in FaceLandMarksArray.leftEyeLower:
            xll, yll = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xll, yll = self.normaliz_pixel(xll, yll, w, h)
            pointsLeftEye.append((xll, yll))
        cv2.drawContours(
            eyes_mask,
            [np.array(pointsRightEye)],
            -1,
            (255, 255, 255),
            -1,
            cv2.LINE_AA,
        )
        cv2.drawContours(
            eyes_mask,
            [np.array(pointsLeftEye)],
            -1,
            (255, 255, 255),
            -1,
            cv2.LINE_AA,
        )
        return eyes_mask

    def __maskEyeBrow(self, face_landmarks):
        h, w, _ = self.faceImage.shape
        pointsRightEyeBrow = []
        pointsLeftEyeBrow = []
        eye_brow_mask = np.zeros((h, w))
        for i in FaceLandMarksArray.rightEyeBrowUpper:
            xru, yru = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xru, yru = self.normaliz_pixel(xru, yru, w, h)
            pointsRightEyeBrow.append((xru, yru))
        for i in FaceLandMarksArray.rightEyeBrowLower:
            xrl, yrl = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xrl, yrl = self.normaliz_pixel(xrl, yrl, w, h)
            pointsRightEyeBrow.append((xrl, yrl))
        for i in FaceLandMarksArray.leftEyeBrowUpper:
            xlu, ylu = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xlu, ylu = self.normaliz_pixel(xlu, ylu, w, h)
            pointsLeftEyeBrow.append((xlu, ylu))
        for i in FaceLandMarksArray.leftEyeBrowLower:
            xll, yll = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xll, yll = self.normaliz_pixel(xll, yll, w, h)
            pointsLeftEyeBrow.append((xll, yll))
        cv2.drawContours(
            eye_brow_mask,
            [np.array(pointsRightEyeBrow)],
            -1,
            (255, 255, 255),
            -1,
            cv2.LINE_AA,
        )
        cv2.drawContours(
            eye_brow_mask,
            [np.array(pointsLeftEyeBrow)],
            -1,
            (255, 255, 255),
            -1,
            cv2.LINE_AA,
        )
        return eye_brow_mask

    def __maskLips(self,face_landmarks):
        h, w, _ = self.faceImage
        pointsLips = []
        lips_mask = np.zeros((h, w))
        for i in FaceLandMarksArray.lipsLowerOuter:
            xl, yl = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xl, yl = self.normaliz_pixel(xl, yl, w, h)
            pointsLips.append((xl, yl))
        for i in FaceLandMarksArray.lips_upper:
            xu, yu = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xu, yu = self.normaliz_pixel(xu, yu, w, h)
            pointsLips.append((xu, yu))

            cv2.drawContours(
                lips_mask,
                [np.array(pointsLips)],
                -1,
                (255, 255, 255),
                -1,
                cv2.LINE_AA,
            )
        return lips_mask

    def apply(self, *args, **kwargs):
        return self

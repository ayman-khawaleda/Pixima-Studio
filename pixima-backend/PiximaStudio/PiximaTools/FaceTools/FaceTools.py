from abc import abstractmethod, ABC

from requests import request
from PiximaTools.abstractTools import Tool
from PiximaStudio.settings import MEDIA_ROOT, MEDIA_URL
from skimage.color import rgb2gray
from PiximaTools.Exceptions import ImageNotSaved, RequiredValue, NoFace
from PiximaTools.AI_Models import (
    FaceSegmentationModel,
    face_mesh_model,
    mp_drawing_styles,
    face_detection_model,
    DrawingSpec,
    draw_landmarks,
)
from rest_framework.serializers import IntegerField, Serializer
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt


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
            face_segmentation = FaceSegmentationModel()

        self.faceMeshDetector = faceMeshDetector
        self.faceDetector = faceDetector
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
            kernal = serialzier.data["Kernal"]
        elif type(kernal.dict()) == dict:

            class KernalSerializer(Serializer):
                Kernal = IntegerField(
                    default=5, required=False, min_value=3, max_value=31
                )

            kernal_serializer = KernalSerializer(data=kernal)
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

            sigmax_serializer = SigmaXSerializer(data=sigmax)
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

            sigmay_serializer = SigmaYSerializer(data=sigmay)
            if not sigmay_serializer.is_valid():
                raise RequiredValue(**sigmay_serializer.errors)
            sigmay = sigmay_serializer.data["SigmaY"]
        self.sigmay = sigmay
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_method(request.data)
            .add_kernal(request.data)
            .add_sigmax(request.data)
            .add_sigmay(request.data)
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

    def __maskEyes(self):
        h, w, _ = self.faceImage.shape
        pointsRightEye = []
        pointsLeftEye = []
        eyes_mask = np.zeros((h, w))
        for facelandmark in self.face_mesh_results:
            self.i += 1
            for i in FaceLandMarksArray.rightEyeUpper:
                xru, yru = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xru, yru = self.normaliz_pixel(xru, yru, w, h)
                pointsRightEye.append((xru, yru))
            for i in FaceLandMarksArray.rightEyeLower:
                xrl, yrl = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xrl, yrl = self.normaliz_pixel(xrl, yrl, w, h)
                pointsRightEye.append((xrl, yrl))
            for i in FaceLandMarksArray.leftEyeUpper:
                xlu, ylu = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xlu, ylu = self.normaliz_pixel(xlu, ylu, w, h)
                pointsLeftEye.append((xlu, ylu))
            for i in FaceLandMarksArray.leftEyeLower:
                xll, yll = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
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

    def __maskEyeBrow(self):
        h, w, _ = self.faceImage.shape
        pointsRightEyeBrow = []
        pointsLeftEyeBrow = []
        eye_brow_mask = np.zeros((h, w))
        for facelandmark in self.face_mesh_results:
            self.i += 1
            for i in FaceLandMarksArray.rightEyeBrowUpper:
                xru, yru = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xru, yru = self.normaliz_pixel(xru, yru, w, h)
                pointsRightEyeBrow.append((xru, yru))
            for i in FaceLandMarksArray.rightEyeBrowLower:
                xrl, yrl = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xrl, yrl = self.normaliz_pixel(xrl, yrl, w, h)
                pointsRightEyeBrow.append((xrl, yrl))
            for i in FaceLandMarksArray.leftEyeBrowUpper:
                xlu, ylu = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xlu, ylu = self.normaliz_pixel(xlu, ylu, w, h)
                pointsLeftEyeBrow.append((xlu, ylu))
            for i in FaceLandMarksArray.leftEyeBrowLower:
                xll, yll = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
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

    def __maskLips(self):
        self.i = 0
        h, w, _ = self.faceImage.shape
        pointsLips = []
        lips_mask = np.zeros((h, w))
        for facelandmark in self.face_mesh_results:
            self.i += 1
            for i in FaceLandMarksArray.lipsLowerOuter:
                xl, yl = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xl, yl = self.normaliz_pixel(xl, yl, w, h)
                pointsLips.append((xl, yl))
            for i in FaceLandMarksArray.lips_upper:
                xu, yu = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
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

    def __model_mask(self):
        h, w, _ = self.faceImage.shape
        model_input_img = cv2.resize(
            rgb2gray(self.faceImage),
            (self.__IMH, self.__IMW),
            interpolation=cv2.INTER_CUBIC,
        ).reshape((self.__IMH, self.__IMW, 1))
        model_mask = self.face_segmentation.predict(model_input_img)
        model_mask = cv2.normalize(model_mask, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        model_mask = cv2.threshold(
            model_mask.reshape((self.__IMH, self.__IMW, 1)),
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]
        return model_mask

    def __mesh_mask(self):
        h, w, _ = self.faceImage.shape
        results = self.faceMeshDetector.process(self.faceImage)
        if not results.multi_face_landmarks:
            raise NoFace(f"No Face Detected In The Image")

        self.face_mesh_results = results.multi_face_landmarks
        for face_landmark in self.face_mesh_results:
            faceovalMask = np.zeros((h, w, 3), np.uint8)
            draw_landmarks(
                image=faceovalMask,
                landmark_list=face_landmark,
                connections=mp_drawing_styles.face_mesh_connections.FACEMESH_FACE_OVAL,
                landmark_drawing_spec=None,
                connection_drawing_spec=DrawingSpec((255, 255, 255), 5, 10),
            )
            ret, thresh = cv2.threshold(
                cv2.cvtColor(faceovalMask, cv2.COLOR_BGR2GRAY),
                127,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU,
            )
            contours, hierarchy = cv2.findContours(
                thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )
            mesh_mask = np.zeros((h, w), np.uint8)
            cv2.drawContours(mesh_mask, contours, 0, (255, 255, 255), -1, cv2.LINE_AA)
            mesh_mask = cv2.resize(mesh_mask, (self.__IMH, self.__IMW))
            mesh_mask = cv2.normalize(
                mesh_mask, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
        return mesh_mask

    def ROI(self):
        face_detection_results = self.faceDetector.process(self.Image)
        for face in face_detection_results.detections:
            h, w, _ = self.Image.shape
            rbb = face.location_data.relative_bounding_box
            self.__rect_start_point = self.normaliz_pixel(rbb.xmin, rbb.ymin, w, h)
            self.__rect_end_point = self.normaliz_pixel(
                rbb.xmin + rbb.width, rbb.ymin + rbb.height, w, h
            )
            self.h_offset = [50, 50]
            self.v_offset = [400, 75]
            self.xstp = (
                0
                if self.__rect_start_point[1] - self.v_offset[0] < 0
                else self.__rect_start_point[1] - self.v_offset[0]
            )
            self.ystp = (
                0
                if self.__rect_start_point[0] - self.h_offset[0] < 0
                else self.__rect_start_point[0] - self.h_offset[0]
            )
            self.xend = self.__rect_end_point[1] + self.v_offset[1]
            self.yend = self.__rect_end_point[0] + self.h_offset[1]
            self.faceImage = self.Image[
                self.xstp : self.xend,
                self.ystp : self.yend,
                :,
            ].copy()

    def __get_face_mask(self):
        model_mask = self.__model_mask()
        mesh_mask = self.__mesh_mask()
        upper_half_mask = model_mask[:128, :]
        upper_half_meshmask = mesh_mask[:128, :]
        lower_half_mask = model_mask[-128:, :]
        lower_half_meshmask = mesh_mask[-128:, :]
        first_op = cv2.bitwise_or(upper_half_mask, upper_half_meshmask)
        second_op = lower_half_meshmask
        res = np.concatenate([first_op, second_op])
        h, w, _ = self.faceImage.shape
        res = cv2.resize(res, (w, h))
        return res

    def constract_final_mask(self):
        self.ROI()
        face_mask = self.__get_face_mask()
        lips_mask = self.__maskLips()
        eyebrow_mask = self.__maskEyeBrow()
        eye_mask = self.__maskEyes()
        or_result = cv2.bitwise_or(lips_mask, eyebrow_mask)
        or_result = cv2.bitwise_or(or_result, eye_mask)
        or_result = self.normalize8(or_result)
        and_result = cv2.bitwise_and(face_mask, cv2.bitwise_not(or_result))
        h, w, _ = self.Image.shape
        self.Mask = np.zeros((w, h), np.uint8)
        self.Mask[self.xstp : self.xend, self.ystp : self.yend] = and_result
        return and_result

    def blur_image(self):
        blured_image = cv2.bilateralFilter(
            self.faceImage, self.kernal, self.sigmax, self.sigmay
        )
        return blured_image

    def apply(self, *args, **kwargs):
        mask = self.constract_final_mask()
        blured_img = self.blur_image()
        temp_image = self.faceImage.copy()
        cond = mask == 255
        temp_image[cond] = blured_img[cond]
        self.Image[
            self.xstp : self.xend,
            self.ystp : self.yend,
            :,
        ] = temp_image
        return self


class WhiteTeethTool(FaceTool):
    def __init__(self, faceMeshDetector=None, saturation=40, brightness=20) -> None:
        if faceMeshDetector is None:
            faceMeshDetector = face_mesh_model
        self.faceMeshDetector = faceMeshDetector
        self.saturation = saturation
        self.brightness = brightness

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_saturation(self, saturation=5, serialzier=None):
        if serialzier:
            saturation = serialzier.data["Saturation"]
        elif type(saturation.dict()) == dict:

            class SaturationSerializer(Serializer):
                Saturation = IntegerField(
                    default=40, required=False, min_value=0, max_value=100
                )

            saturation_serializer = SaturationSerializer(data=saturation)
            if not saturation_serializer.is_valid():
                raise RequiredValue(**saturation_serializer.errors)
            saturation = saturation_serializer.data["Saturation"]
        self.saturation = saturation
        return self

    def add_brightness(self, brightness=5, serialzier=None):
        if serialzier:
            brightness = serialzier.data["Brightness"]
        elif type(brightness.dict()) == dict:

            class BrightnessSerializer(Serializer):
                Brightness = IntegerField(
                    default=20, required=False, min_value=0, max_value=100
                )

            brightness_serializer = BrightnessSerializer(data=brightness)
            if not brightness_serializer.is_valid():
                raise RequiredValue(**brightness_serializer.errors)
            brightness = brightness_serializer.data["Brightness"]
        self.brightness = brightness
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_saturation(request.data)
            .add_brightness(request.data)
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_brightness(serialzier=serializer)
            .add_brightness(serialzier=serializer)
        )

    def __process_face(self, th=100):
        self.Mask = np.zeros(self.Image.shape[:2], np.uint8)
        self.results = self.faceMeshDetector.process(self.Image)
        if not self.results.multi_face_landmarks:
            raise NoFace("No Face Detected In The Image")
        for face_landmarks in self.results.multi_face_landmarks:
            self.__make_mask_teeth(face_landmarks, th)

    def __make_mask_teeth(self, face_landmarks, th=100):
        h, w, _ = self.Image.shape

        pointsTeeth = []
        self.min_y_teeth = h
        self.max_y_teeth = 0
        self.min_x_teeth = int(face_landmarks.landmark[78].x * w)
        self.max_x_teeth = int(face_landmarks.landmark[308].x * w)
        for i in FaceLandMarksArray.lips_lower:
            xl, yl = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xl, yl = self.normaliz_pixel(xl, yl, w, h)
            if yl > self.max_y_teeth:
                self.max_y_teeth = yl
            pointsTeeth.append((xl, yl))
        for i in FaceLandMarksArray.lips_upper:
            xu, yu = face_landmarks.landmark[i].x, face_landmarks.landmark[i].y
            xu, yu = self.normaliz_pixel(xu, yu, w, h)
            if yu < self.min_y_teeth:
                self.min_y_teeth = yu
            pointsTeeth.append((xu, yu))

            if self.max_y_teeth - self.min_y_teeth > 10:
                cv2.drawContours(
                    self.Mask,
                    [np.array(pointsTeeth)],
                    -1,
                    (255, 255, 255),
                    -1,
                    cv2.LINE_AA,
                )

        self.teeth = self.Image[
            self.min_y_teeth : self.max_y_teeth, self.min_x_teeth : self.max_x_teeth, :
        ].copy()

        self.teethmask = self.Mask[
            self.min_y_teeth : self.max_y_teeth, self.min_x_teeth : self.max_x_teeth
        ].copy()

        teeth_gray = cv2.cvtColor(self.teeth, cv2.COLOR_RGB2GRAY)
        ret, th1 = cv2.threshold(teeth_gray, th, 255, cv2.THRESH_BINARY)
        self.teethmask = cv2.bitwise_and(th1, self.teethmask)

    def __process_teeth(self):
        teeth_hsv = cv2.cvtColor(self.teeth, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(teeth_hsv)
        s[(self.teethmask == 255) & (s > self.saturation)] -= self.saturation
        v[(self.teethmask == 255) & (v < self.brightness)] += self.brightness
        teeth_hsv = cv2.merge([h, s, v])
        self.teeth = cv2.cvtColor(teeth_hsv, cv2.COLOR_HSV2RGB)


    def apply(self, *args, **kwargs):
        self.__process_face()
        self.__process_teeth()

        self.Image[
            self.min_y_teeth : self.max_y_teeth, self.min_x_teeth : self.max_x_teeth, :
        ] = self.teeth

        self.Mask[
            self.min_y_teeth : self.max_y_teeth, self.min_x_teeth : self.max_x_teeth
        ] = self.teethmask

        return self

class ColorLipsTool(FaceTool):
    def __init__(self, faceMeshDetector=None, saturation=0, color=0) -> None:
        if faceMeshDetector is None:
            faceMeshDetector = face_mesh_model
        self.faceMeshDetector = faceMeshDetector
        self.saturation = saturation
        self.color = color

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_saturation(self, saturation=5, serialzier=None):
        if serialzier:
            saturation = serialzier.data["Saturation"]
        elif type(saturation.dict()) == dict:

            class SaturationSerializer(Serializer):
                Saturation = IntegerField(
                    default=0, required=False, min_value=-100, max_value=100
                )

            saturation_serializer = SaturationSerializer(data=saturation)
            if not saturation_serializer.is_valid():
                raise RequiredValue(**saturation_serializer.errors)
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
                raise RequiredValue(**color_serializer.errors)
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
    
    def __lips_mask(self):
        h, w, _ = self.Image.shape
        results = self.faceMeshDetector.process(self.Image)
        if results.multi_face_landmarks:
            raise NoFace(f"No Face Detected In The Image")

        pointsLips_outter = []
        pointsLips_inner = []
        lips_mask = np.zeros((h, w))
        for facelandmark in results.multi_face_landmarks:
            for i in self.lipsLowerOuter:
                xl, yl = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xl, yl = self.normaliz_pixel(xl, yl, w, h)
                pointsLips_outter.append((xl, yl))
            for i in self.lipsUpperOuter:
                xu, yu = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xu, yu = self.normaliz_pixel(xu, yu, w, h)
                pointsLips_outter.append((xu, yu))

            for i in self.lips_lower:
                xl, yl = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xl, yl = self.normaliz_pixel(xl, yl, w, h)
                pointsLips_inner.append((xl, yl))
            for i in self.lips_upper:
                xu, yu = (
                    facelandmark.landmark[i].x,
                    facelandmark.landmark[i].y,
                )
                xu, yu = self.normaliz_pixel(xu, yu, w, h)
                pointsLips_inner.append((xu, yu))

            cv2.drawContours(
                lips_mask,
                [np.array(pointsLips_outter)],
                -1,
                (255, 255, 255),
                -1,
                cv2.LINE_AA,
            )
            
            cv2.drawContours(
                lips_mask,
                [np.array(pointsLips_inner)],
                -1,
                (0,0,0),
                -1,
                cv2.LINE_AA,
            )
        self.lips_mask = lips_mask
        

    def apply(self,*args,**kwargs):
        return self
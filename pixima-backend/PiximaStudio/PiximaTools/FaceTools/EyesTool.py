from abc import abstractmethod, ABC
from .FaceTools import FaceTool
from PiximaTools.Exceptions import NoFace, RequiredValue
from PiximaTools.AI_Models import face_detection_model, face_mesh_model
import cv2
import numpy as np
import mediapipe as mp
import decimal
from rest_framework.serializers import ListField, IntegerField, Serializer


class EyesTool(FaceTool):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass


class EyesColorTool(EyesTool):
    def __init__(self, faceMeshDetector=None):
        if faceMeshDetector is None:
            faceMeshDetector = face_mesh_model
        self.faceMeshDetector = faceMeshDetector

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_color(self, color={"Color": [0]}, serializer=None):
        if serializer is not None:
            color = serializer.data["Color"]
        elif type(color.dict()) == dict:

            class ColorSerializer(Serializer):
                Color = ListField(
                    child=IntegerField(default=0, min_value=0, max_value=255),
                    min_length=1,
                    max_length=2,
                )

            color_serializer = ColorSerializer(data=color)
            if not color_serializer.is_valid():
                raise RequiredValue("Color List Requierd")
            color = color_serializer.data["Color"]
            print(color)
        else:
            raise RequiredValue("Color Should Be Dict Or List")
        self.color = color
        return self

    def add_saturation(self, saturation={"Saturation": [0]}, serializer=None):
        if serializer is not None:
            saturation = serializer.data["Saturation"]
        elif type(saturation.dict()) == dict:

            class SaturationSerializer(Serializer):
                Saturation = ListField(
                    child=IntegerField(default=0, min_value=0, max_value=100),
                    min_length=1,
                    max_length=2,
                )

            saturation_serializer = SaturationSerializer(data=saturation)
            if not saturation_serializer.is_valid():
                raise RequiredValue("Saturation List Requierd")
            saturation = saturation_serializer.data["Saturation"]
            print(saturation)
        else:
            raise RequiredValue("Saturation Should Be Dict Or List")
        self.saturation = saturation
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_color(request.data)
            .add_saturation(request.data)
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_color(serializer=serializer)
            .add_saturation(serializer=serializer)
        )

    def apply(self, *args, **kwargs):
        """
        \nkwargs:
            \nFile: Path For The Image To Be Modifed.
        """
        if "File" in kwargs:
            self.path = kwargs["File"]
            self.Image = cv2.cvtColor(cv2.imread(self.path), cv2.COLOR_BGR2RGB)
        results = self.faceMeshDetector.process(self.Image)
        if not results.multi_face_landmarks:
            raise NoFace(f"No Face Detected In The Image")

        h, w, _ = self.Image.shape
        self.Mask = np.zeros((h, w))

        self.__ri_list, self.__li_list = [], []
        for face_landmarks in results.multi_face_landmarks:
            self.__is_right_open, self.__is_left_open = self.__are_eyes_open(
                face_landmarks
            )
            right_iris_mask, left_iris_mask = self.__extract_iris_mask(face_landmarks)
            self.__color_eye(
                right_iris_mask=right_iris_mask,
                left_iris_mask=left_iris_mask,
            )
        return self

    def __are_eyes_open(self, face_landmarks, dist: int = 15):
        right_min_p, right_max_p, left_min_p, left_max_p = (
            decimal.MAX_EMAX,
            0,
            decimal.MAX_EMAX,
            0,
        )
        mp_face_mesh = mp.solutions.face_mesh
        h, w, _ = self.Image.shape
        for tup1, tup2 in zip(
            mp_face_mesh.FACEMESH_RIGHT_EYE, mp_face_mesh.FACEMESH_LEFT_EYE
        ):
            # Finding Both minimum & maximum values of right eyelid
            sor_idx, _ = tup1
            source = face_landmarks.landmark[sor_idx]
            norm = self.normaliz_pixel(source.x, source.y, w, h)
            if norm[1] > right_max_p:
                right_max_p = norm[1]
            if norm[1] < right_min_p:
                right_min_p = norm[1]

            # Finding Both minimum & maximum values of left eyelid
            sor_idx, _ = tup2
            source = face_landmarks.landmark[sor_idx]
            norm = self.normaliz_pixel(source.x, source.y, w, h)
            if norm[1] > left_max_p:
                left_max_p = norm[1]
            if norm[1] < left_min_p:
                left_min_p = norm[1]

        # Calculating the Distance between the two values
        return (right_max_p - right_min_p > dist, left_max_p - left_min_p > dist)

    def __extract_iris_mask(self, face_landmarks, k: tuple = (3, 3), iter: int = 1):
        h, w, _ = self.Image.shape
        right_th, left_th = None, None

        # Extract The Left (Iris & Eye) mask With Bin_Inv and Otsu
        # Than Generate Ellipse Mask have the same shape of Iris mask
        # Do bitwise_and Between Previous masks To make sure I have the right shape of Iris
        # Do MORPH_DILATE to expand the mask and getrid of balckholes (NOTE: Have better results than MORPH_OPENING)
        # End up with bitwise_and between Ellipse Mask and Previous mask
        if self.__is_left_open:
            for tup in mp.solutions.face_mesh.FACEMESH_LEFT_IRIS:
                sor_idx, _ = tup
                source = face_landmarks.landmark[sor_idx]
                rel_source = self.normaliz_pixel(source.x, source.y, w, h)
                self.__li_list.append(rel_source)
            self.left_iris = self.Image[
                self.__li_list[1][1] : self.__li_list[2][1],
                self.__li_list[0][0] : self.__li_list[3][0],
                :,
            ].copy()
            _, left_th = cv2.threshold(
                cv2.cvtColor(self.left_iris, cv2.COLOR_RGB2GRAY),
                0,
                255,
                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
            )
            lellipse = 255 * cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (left_th.shape[1], left_th.shape[0])
            ).astype(np.uint8)
            left_th = cv2.bitwise_and(left_th, lellipse)
            left_th = cv2.morphologyEx(left_th, cv2.MORPH_DILATE, k, iterations=iter)
            left_th = cv2.bitwise_and(left_th, lellipse)
            self.Mask[
                self.__li_list[1][1] : self.__li_list[2][1],
                self.__li_list[0][0] : self.__li_list[3][0],
            ] = left_th.copy()
        # Extract The Right (Iris & Eye) mask With Bin_Inv and Otsu
        if self.__is_right_open:
            for tup in mp.solutions.face_mesh.FACEMESH_RIGHT_IRIS:
                sor_idx, _ = tup
                source = face_landmarks.landmark[sor_idx]
                rel_source = self.normaliz_pixel(source.x, source.y, w, h)
                self.__ri_list.append(rel_source)

            self.right_iris = self.Image[
                self.__ri_list[3][1] : self.__ri_list[1][1],
                self.__ri_list[2][0] : self.__ri_list[0][0],
                :,
            ].copy()

            _, right_th = cv2.threshold(
                cv2.cvtColor(self.right_iris, cv2.COLOR_RGB2GRAY),
                0,
                255,
                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
            )
            rellipse = 255 * cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (right_th.shape[1], right_th.shape[0])
            ).astype(np.uint8)
            right_th = cv2.bitwise_and(right_th, rellipse)
            right_th = cv2.morphologyEx(right_th, cv2.MORPH_DILATE, k, iterations=iter)
            right_th = cv2.bitwise_and(right_th, rellipse)
            self.Mask[
                self.__ri_list[3][1] : self.__ri_list[1][1],
                self.__ri_list[2][0] : self.__ri_list[0][0],
            ] = right_th.copy()
        return right_th, left_th

    def __color_eye(self, right_iris_mask, left_iris_mask):

        if self.__is_right_open:
            # Right Eye Iris Processing
            hsv_right_iris = cv2.cvtColor(self.right_iris, cv2.COLOR_RGB2HSV)
            r_h, r_s, r_v = cv2.split(hsv_right_iris)
            temp = r_h.copy()
            temp[right_iris_mask == 255] = (
                self.color[0] if len(self.color) == 2 else self.color[0]
            )
            r_s[right_iris_mask == 255] += (
                self.saturation[0] if len(self.saturation) == 2 else self.saturation[0]
            )
            r_s[right_iris_mask == 255] = np.clip(r_s[right_iris_mask == 255], 0, 255)
            temp = cv2.cvtColor(cv2.merge([temp, r_s, r_v]), cv2.COLOR_HSV2RGB)
            self.Image[
                self.__ri_list[3][1] : self.__ri_list[1][1],
                self.__ri_list[2][0] : self.__ri_list[0][0],
                :,
            ] = temp

        if self.__is_left_open:
            # Left Eye Iris Processing
            hsv_left_iris = cv2.cvtColor(self.left_iris, cv2.COLOR_RGB2HSV)
            l_h, l_s, l_v = cv2.split(hsv_left_iris)
            temp = l_h.copy()
            temp[left_iris_mask == 255] = (
                self.color[1] if len(self.color) == 2 else self.color[0]
            )
            l_s[left_iris_mask == 255] += (
                self.saturation[1] if len(self.saturation) == 2 else self.saturation[0]
            )
            l_s[left_iris_mask == 255] = np.clip(l_s[left_iris_mask == 255], 0, 255)
            temp = cv2.cvtColor(cv2.merge([temp, l_s, l_v]), cv2.COLOR_HSV2RGB)
            self.Image[
                self.__li_list[1][1] : self.__li_list[2][1],
                self.__li_list[0][0] : self.__li_list[3][0],
                :,
            ] = temp

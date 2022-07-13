from abc import abstractmethod, ABC
from .FaceTools import FaceTool
from PiximaTools.Exceptions import NoFace, RequiredValue
from PiximaTools.AI_Models import face_detection_model, face_mesh_model
import cv2
import numpy as np
import mediapipe as mp
import decimal
from rest_framework.serializers import ListField, IntegerField, Serializer, FloatField


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
                raise RequiredValue("Color List Is Required")
            color = color_serializer.data["Color"]
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
                raise RequiredValue("Saturation List Is Required")
            saturation = saturation_serializer.data["Saturation"]
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


class EyesResizeTool(FaceTool):
    def __init__(self, factor=1.1, radius=75,faceDetector=None,faceMeshDetector=None):
        self.factor = factor
        self.radius = radius
        
        if faceDetector is None:
            faceDetector = face_detection_model
        if faceMeshDetector is None:
            faceMeshDetector = face_mesh_model

        self.faceDetector = faceDetector
        self.faceMeshDetector = faceMeshDetector

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

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_factor(request.data)
            .add_radius(request.data)
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_factor(serializer=serializer)
            .add_radius(serializer=serializer)
        )

    def apply(self,*args,**kwargs):
        """kwargs:
            \nFile: Path For The Image To Be Modifed.
            \nRadius: The Region Around The Eye Where All Processing Are Done.
        """
        if "File" in kwargs:
            self.path = kwargs["File"]
            self.Image = cv2.cvtColor(cv2.imread(self.path), cv2.COLOR_BGR2RGB)
        if "Radius" in kwargs:
            self.radius = kwargs["Radius"]
        
        results = self.faceDetector.process(self.Image)
        rows, cols, _ = self.Image.shape
        if not results.detections:
            raise NoFace(f'No Faces Detected In Image')

        for detection in results.detections:
            rbb = detection.location_data.relative_bounding_box
            rect_start_point = self.normaliz_pixel(rbb.xmin, rbb.ymin, cols, rows)
            rect_end_point = self.normaliz_pixel(
                rbb.xmin + rbb.width, rbb.ymin + rbb.height, cols, rows
            )
            faceROI = self.Image[
                rect_start_point[1] : rect_end_point[1],
                rect_start_point[0] : rect_end_point[0],
                :,
            ].copy()
            mesh_result = self.faceMeshDetector.process(faceROI)
            h, w, _ = faceROI.shape
            right_eye, left_eye = self.__get_eyes_key_points(mesh_result, w, h)
            self.__create_index_maps(h, w)
            self.__edit_area(right_eye,left_eye)
            self.__smothe_border(right_eye, left_eye)
            self.__remaping(faceROI, rect_start_point, rect_end_point)
        return self

    def __get_eyes_key_points(self, mesh, w, h):
        mp_face_mesh = mp.solutions.face_mesh
        right_eye_list, left_eye_list = [], []
        for face_landmarks in mesh.multi_face_landmarks:
            for tup in mp_face_mesh.FACEMESH_RIGHT_EYE:
                sor_idx, tar_idx = tup
                source = face_landmarks.landmark[sor_idx]
                target = face_landmarks.landmark[tar_idx]
                rel_source = (int(source.x * w), int(source.y * h))
                rel_target = (int(target.x * w), int(target.y * h))
                right_eye_list.append(rel_source)
                right_eye_list.append(rel_target)

            for tup in mp_face_mesh.FACEMESH_LEFT_EYE:
                sor_idx, tar_idx = tup
                source = face_landmarks.landmark[sor_idx]
                target = face_landmarks.landmark[tar_idx]
                rel_source = (int(source.x * w), int(source.y * h))
                rel_target = (int(target.x * w), int(target.y * h))
                left_eye_list.append(rel_source)
                left_eye_list.append(rel_target)
            right_eye_list.sort(key=lambda x: x[1])
            right_eye_minh, right_eye_maxh = right_eye_list[0], right_eye_list[-1]
            right_eye_list.sort(key=lambda x: x[0])
            right_eye_minw, right_eye_maxw = right_eye_list[0], right_eye_list[-1]
            right_eye = (
                (right_eye_minw[0] + right_eye_maxw[0]) // 2,
                (right_eye_minh[1] + right_eye_maxh[1]) // 2,
            )

            left_eye_list.sort(key=lambda x: x[1])
            left_eye_minh, left_eye_maxh = left_eye_list[0], left_eye_list[-1]
            left_eye_list.sort(key=lambda x: x[0])
            left_eye_minw, left_eye_maxw = left_eye_list[0], left_eye_list[-1]
            left_eye = (
                (left_eye_minw[0] + left_eye_maxw[0]) // 2,
                (left_eye_minh[1] + left_eye_maxh[1]) // 2,
            )
            return right_eye, left_eye

    def __create_index_maps(self, h, w):
        xs = np.arange(0, h, 1, dtype=np.float32)
        ys = np.arange(0, w, 1, dtype=np.float32)
        self.__right_map_x, self.__right_map_y = np.meshgrid(xs, ys)
        self.__left_map_x, self.__left_map_y = np.meshgrid(xs, ys)

    def __edit_area(self, right_eye, left_eye):
        for i in range(-self.radius, self.radius):
            for j in range(-self.radius, self.radius):
                if i**2 + j**2 > self.radius**2:
                    continue
                if i > 0:
                    self.__right_map_y[right_eye[1] + i][right_eye[0] + j] = (
                        right_eye[1] + (i / self.radius) ** self.factor * self.radius
                    )
                    self.__left_map_y[left_eye[1] + i][left_eye[0] + j] = (
                        left_eye[1] + (i / self.radius) ** self.factor * self.radius
                    )
                if i < 0:
                    self.__right_map_y[right_eye[1] + i][right_eye[0] + j] = (
                        right_eye[1] - (-i / self.radius) ** self.factor * self.radius
                    )
                    self.__left_map_y[left_eye[1] + i][left_eye[0] + j] = (
                        left_eye[1] - (-i / self.radius) ** self.factor * self.radius
                    )
                if j > 0:
                    self.__right_map_x[right_eye[1] + i][right_eye[0] + j] = (
                        right_eye[0] + (j / self.radius) ** self.factor * self.radius
                    )
                    self.__left_map_x[left_eye[1] + i][left_eye[0] + j] = (
                        left_eye[0] + (j / self.radius) ** self.factor * self.radius
                    )
                if j < 0:
                    self.__right_map_x[right_eye[1] + i][right_eye[0] + j] = (
                        right_eye[0] - (-j / self.radius) ** self.factor * self.radius
                    )
                    self.__left_map_x[left_eye[1] + i][left_eye[0] + j] = (
                        left_eye[0] - (-j / self.radius) ** self.factor * self.radius
                    )
    def __smothe_border(self,right_eye,left_eye, k=5, xspace=10, yspace=10, sigmax=0):
        r = self.radius
        yr, xr = right_eye
        yl, xl = left_eye
        lUr = [yr - r - yspace, xr - r - xspace]  # Left Upper Right Eye
        rLr = [yr + r + yspace, xr + r + xspace]  # Right Lower Right Eye
        lUl = [yl - r - yspace, xl - r - xspace]  # Left Upper Left Eye
        rLl = [yl + r + yspace, xl + r + xspace]  # Right Lower Left  Eye
        self.__right_map_x[lUr[1] : rLr[1], lUr[0] : rLr[0]] = cv2.GaussianBlur(
            self.__right_map_x[lUr[1] : rLr[1], lUr[0] : rLr[0]].copy(), (k,k), sigmax
        )

        self.__right_map_y[lUr[1] : rLr[1], lUr[0] : rLr[0]] = cv2.GaussianBlur(
            self.__right_map_y[lUr[1] : rLr[1], lUr[0] : rLr[0]].copy(), (k,k), sigmax
        )

        self.__left_map_x[lUl[1] : rLl[1], lUl[0] : rLl[0]] = cv2.GaussianBlur(
            self.__left_map_x[lUl[1] : rLl[1], lUl[0] : rLl[0]].copy(), (k,k), sigmax
        )
        self.__left_map_y[lUl[1] : rLl[1], lUl[0] : rLl[0]] = cv2.GaussianBlur(
            self.__left_map_y[lUl[1] : rLl[1], lUl[0] : rLl[0]].copy(), (k,k), sigmax
        )

    def __remaping(self,faceROI,rect_start_point,rect_end_point):
        warped = cv2.remap(faceROI, self.__right_map_x, self.__right_map_y, cv2.INTER_CUBIC)
        warped = cv2.remap(warped, self.__left_map_x, self.__left_map_y, cv2.INTER_CUBIC)

        self.Image[
            rect_start_point[1] : rect_end_point[1],
            rect_start_point[0] : rect_end_point[0],
            :,
        ] = warped

from rest_framework.serializers import IntegerField, FloatField, Serializer
from .FaceTools import FaceTool
from PiximaTools.AI_Models import face_detection_model
from PiximaTools.Exceptions import NoFace, RequiredValue
import cv2
import numpy as np

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
        """kwargs:
        \nFile: Path For The Image To Be Modifed.
        \nRadius: The Region Around The Nose Where All Processing Are Done.
        """
        if "File" in kwargs:
            self.Image = cv2.cvtColor(cv2.imread(kwargs["File"]), cv2.COLOR_BGR2RGB)
        if "Radius" in kwargs:
            self.radius = kwargs["Radius"]

        results = self.faceDetector.process(self.Image)
        if not results:
            raise NoFace("No Face Detected In Image")
        rows, cols, _ = self.Image.shape
        rbb = results.detections[0].location_data.relative_bounding_box
        nose_p = results.detections[0].location_data.relative_keypoints[2]

        nose_p = self.normaliz_pixel(nose_p.x, nose_p.y, cols, rows)
        face_upper = self.normaliz_pixel(rbb.xmin, rbb.ymin, cols, rows)
        face_lower = self.normaliz_pixel(
            rbb.xmin + rbb.width, rbb.ymin + rbb.height, cols, rows
        )
        face = self.Image[
            face_upper[1] : face_lower[1], face_upper[0] : face_lower[0], :
        ].copy()
        self.Image[nose_p[1], nose_p[0], :] = (255, 0, 0)

        h, w = face.shape[0], face.shape[1]
        self.nose_p = self.__detect_nose_tip(face_upper, face_lower)
        self.nose_p += np.array([self.y, self.x])
        self.__create_index_map(h, w)
        self.__edit_nose_area()
        self.__smothe_border()
        self.__remaping(face, face_upper, face_lower)
        return self

    def __detect_nose_tip(self, face_upper, face_lower):
        subface = self.Image[
            face_upper[1] : face_lower[1], face_upper[0] : face_lower[0], :
        ].copy()
        index = np.where(subface[:, :, 0] == 255)
        p = 0
        for x, y in zip(index[0], index[1]):
            r, g, b = subface[x, y, :]
            if r == 255 and g == 0 and b == 0:
                p = np.array([y, x])
        if type(p) is int:
            if p == 0:
                raise Exception("No Nose Point found for face")
        return p

    def __create_index_map(self, h, w):
        xs = np.arange(0, h, 1, dtype=np.float32)
        ys = np.arange(0, w, 1, dtype=np.float32)
        self.nose_map_x, self.nose_map_y = np.meshgrid(xs, ys)
    
    def __edit_nose_area(self):
        for i in np.arange(-self.radius, self.radius):
            for j in np.arange(-self.radius, self.radius):
                if i**2 + j**2 > self.radius**2:
                    continue
                if i > 0:
                    self.nose_map_y[self.nose_p[1] + i][self.nose_p[0] + j] = (
                        self.nose_p[1] + (i / self.radius) ** self.factor * self.radius
                    )
                if i < 0:
                    self.nose_map_y[self.nose_p[1] + i][self.nose_p[0] + j] = (
                        self.nose_p[1] - (-i / self.radius) ** self.factor * self.radius
                    )
                if j > 0:
                    self.nose_map_x[self.nose_p[1] + i][self.nose_p[0] + j] = (
                        self.nose_p[0] + (j / self.radius) ** self.factor * self.radius
                    )
                if j < 0:
                    self.nose_map_x[self.nose_p[1] + i][self.nose_p[0] + j] = (
                        self.nose_p[0] - (-j / self.radius) ** self.factor * self.radius
                    )

    def __smothe_border(self, k=3, xspace=10, yspace=10, sigmax=0):
        y, x = self.nose_p
        r = self.radius
        lU = [y - r - yspace, x - r - xspace]  # Left Upper
        rL = [y + r + yspace, x + r + xspace]  # Right Lower
        self.nose_map_x[lU[1] : rL[1], lU[0] : rL[0]] = cv2.GaussianBlur(
            self.nose_map_x[lU[1] : rL[1], lU[0] : rL[0]].copy(), (k, k), sigmax
        )
        self.nose_map_y[lU[1] : rL[1], lU[0] : rL[0]] = cv2.GaussianBlur(
            self.nose_map_y[lU[1] : rL[1], lU[0] : rL[0]].copy(), (k, k), sigmax
        )

    def __remaping(self, face, face_upper, face_lower):
        warped = cv2.remap(face, self.nose_map_x, self.nose_map_y, cv2.INTER_CUBIC)
        self.Image[
            face_upper[1] : face_lower[1], face_upper[0] : face_lower[0], :
        ] = warped

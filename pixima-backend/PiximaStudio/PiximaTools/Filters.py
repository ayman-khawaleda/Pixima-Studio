from abc import abstractmethod
from random import Random
from select import KQ_NOTE_LOWAT
from unittest.mock import NonCallableMagicMock

from sklearn.feature_selection import SelectFdr
from PiximaTools.abstractTools import Tool
import cv2
import numpy as np


class Filter(Tool):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass


class GlitchFilter(Filter):
    def __init__(self, shift=20, step=15, density=5) -> None:
        self.shift = shift
        self.step = step
        self.density = density

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_shift(serializer=serializer)
            .add_step(serializer=serializer)
            .add_density(serializer=serializer)
        )

    def add_shift(self, shift=20, serializer=None):
        if serializer is not None:
            shift = serializer.data["Shift"]
        if type(shift) == str:
            shift = int(shift)
        if shift > 50 or shift < 5:
            shift = 20
        self.shift = shift
        return self

    def add_step(self, step=15, serializer=None):
        if serializer is not None:
            step = serializer.data["Step"]
        if type(step) == str:
            step = int(step)
        if step > 25 or step < 5:
            step = 20
        self.step = step
        return self

    def add_density(self, density=5, serializer=None):
        if serializer is not None:
            density = serializer.data["Density"]
        if type(density) == str:
            density = int(density)
        if density > 50 or density < 0:
            density = 5
        self.density = density
        return self

    def apply(self, *args, **kwargs):
        img = self.Image
        h, w, _ = img.shape
        kernal = np.zeros((h, w), np.uint8)
        thickness = 2
        if h > 1000:
            thickness = 4
        list_range = []
        for i in range(0, h, self.step):
            list_range.append((i - self.step, i))
            kernal = cv2.line(
                kernal, (0, int(i)), (int(w), int(i)), (255, 255, 255), thickness
            )
        kernal = cv2.merge([kernal, kernal, kernal])
        cyan_img = img.copy()
        pink_img = img.copy()
        pink_img[:, :, 1] = 0
        cyan_img[:, :, 0] = 0
        pink_img = np.roll(pink_img, self.shift, 1)
        cyan_img = np.roll(cyan_img, -self.shift, 1)
        new_img = cv2.addWeighted(img, 0.5, pink_img, 0.9, 0)
        new_img = cv2.addWeighted(new_img, 0.5, cyan_img, 0.75, 0)
        new_img = cv2.addWeighted(
            new_img,
            0.85,
            kernal,
            0.15,
            0,
        )
        for i in Random().choices(list_range, k=self.density):
            down = i[0]
            upper = i[0] + (self.step * Random().randint(0, 3))
            new_img[down:upper, :, :] = np.roll(
                new_img[down:upper, :, :], Random().randint(-100, 100), 1
            )
        self.Image = new_img
        return self


class CirclesFilter(Filter):
    def __init__(self, facekey_options=["RightEye", "LefyEye", "Nose"]) -> None:
        self.face_key = "None"
        self.x = -1
        self.y = -1
        self.radius = 5
        self.facekey_options = facekey_options

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_center(self, x=0, y=0, serializer=None):
        if serializer is not None:
            x, y = serializer.data["X"], serializer.data["Y"]
        if type(x) == str or type(y) == str:
            x, y = int(x), int(y)
        if x <= -1 or y <= -1:
            x, y = -1, -1
        return self

    def add_facekey(self, face_key="RightEye", serializer=None):
        if serializer is not None:
            face_key = serializer.data["FaceKey"]
        if face_key not in self.facekey_options:
            face_key = "RightEye"
        self.face_key = face_key
        return self

    def add_radius(self, radius=15, serializer=None):
        if serializer is not None:
            radius = serializer.data["Radius"]
        if type(radius) == str:
            radius = int(radius)
        if radius > 30 or radius < 5:
            radius = 15
        return self

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_center(serializer=serializer)
            .add_facekey(serializer=serializer)
            .add_radius(serializer=serializer)
        )

    def apply(self, *args, **kwargs):
        return self
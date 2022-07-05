from abc import abstractmethod
from PiximaTools.abstractTools import Tool
import numpy as np
import cv2
from skimage.transform import rotate

class PhotoTool(Tool):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass


class CropTool(PhotoTool):
    def __init__(self, cords: list = None, ratio: str = "1:1") -> None:
        self.cords = cords
        self.ratio = ratio

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_cords(self, X1=-1, X2=-1, Y1=-1, Y2=-1, serializer=None):
        if serializer is not None:
            X1, X2, Y1, Y2 = (
                int(serializer.data["X1"]),
                int(serializer.data["X2"]),
                int(serializer.data["Y1"]),
                int(serializer.data["Y2"]),
            )
        self.cords = [X1, X2, Y1, Y2]
        return self

    def check_cords(self):
        if self.cords is None:
            return False
        if any([x <= -1 for x in self.cords]):
            return False
        return True

    def add_ratio(self, ratio: str = None, serializer=None):
        if serializer is not None:
            ratio = serializer.data["Ratio"]
        self.ratio = ratio
        return self

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_cords(serializer=serializer)
            .add_ratio(serializer=serializer)
        )

    def apply(self, *args, **kwargs):
        if self.check_cords():
            x1, x2, y1, y2 = self.cords
            croped_img = self.Image.copy()
            croped_img = croped_img[x1:x2, y1:y2, :]
            self.Image = croped_img

        else:
            value = self.ratio
            aspect_ratio = 1
            if value == "4:3":
                aspect_ratio = 3 / 4
            elif value == "16:9":
                aspect_ratio = 9 / 16
            elif value == "9:16":
                aspect_ratio = 16 / 9
            elif value == "5:4":
                aspect_ratio = 4 / 5

            h, w, _ = self.Image.shape
            width = int(np.min([w, h * aspect_ratio]))
            high = int(np.min([w / aspect_ratio, h]))
            left = int((w - width) / 2)
            top = int((h - high) / 2)
            croped_img = self.Image.copy()
            croped_img = croped_img[left : left + width, top : top + high]
            self.Image = croped_img

        return self


class FlipTool(PhotoTool):
    def __init__(self, direction: str = None) -> None:
        if direction is None:
            self.direction = "Hor"
        else:
            self.direction = direction

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_direction(self, dir: str = "Hor", serializer=None):
        if serializer is not None:
            dir = serializer.data["Direction"]
        self.direction = dir
        return self

    def serializer2data(self, serializer):
        return super().serializer2data(serializer).add_direction(serializer=serializer)

    def apply(self, *args, **kwargs):
        if self.direction == "Hor":
            self.Image = cv2.flip(self.Image, 0)
        elif self.direction == "Ver":
            self.Image = cv2.flip(self.Image, 1)
        return self


class RotatTool(PhotoTool):
    def __init__(self, angle: int = 90, clock_wise: bool = False) -> None:
        self.angle = angle
        self.clock_wise = clock_wise

    def __call__(self, *args, **kwargs):
        return self.apply()

    def add_angle(self, angle: str = 90, serializer=None):
        if serializer is not None:
            angle = serializer.data["Angle"]
        self.angle = angle
        return self

    def add_clock_wise(self, clock_wise: bool = False, serializer=None):
        if serializer is not None:
            clock_wise = serializer.data["ClockWise"]
        self.clock_wise = clock_wise
        return self

    def add_area_mode(self,mode:str="constant",serializer=None):
        if serializer is not None:
            mode = serializer.data["AreaMode"]
        self.add_area_mode = mode
        return self

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_angle(serializer=serializer)
            .add_clock_wise(serializer=serializer)
            .add_area_mode(serializer=serializer)
        )

    def apply(self, *args, **kwargs):
        angle = self.add_angle
        if self.clock_wise:
            angle *=-1
        self.Image = rotate(self.Image,angle=angle,resize=True,mode=self.add_area_mode)
        return self

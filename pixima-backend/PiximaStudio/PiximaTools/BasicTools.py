from abc import abstractmethod
from PiximaTools.abstractTools import Tool
import numpy as np
import cv2
from skimage.transform import rotate
import PIL


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

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_ratio(request.data.setdefault("Ratio", "1:1"))
            .add_cords(
                X1=request.data.setdefault("X1", -1),
                X2=request.data.setdefault("X2", -1),
                Y1=request.data.setdefault("Y1", -1),
                Y2=request.data.setdefault("Y2", -1),
            )
        )

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

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_direction(request.data.setdefault("Direction", "Hor"))
        )

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

    def add_angle(self, angle=90, serializer=None):
        if serializer is not None:
            angle = serializer.data["Angle"]
        if angle == "":
            angle = 90
        if type(angle) == str:
            angle = int(angle)
        self.angle = angle
        return self

    def add_clock_wise(self, clock_wise=False, serializer=None):
        if serializer is not None:
            clock_wise = serializer.data["ClockWise"]
        self.clock_wise = bool(clock_wise)
        return self

    def add_area_mode(self, mode: str = "constant", serializer=None):
        if serializer is not None:
            mode = serializer.data["AreaMode"]
        if mode == "":
            mode = "constant"
        self.add_area_mode = mode
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_angle(request.data.setdefault("Angle", 90))
            .add_clock_wise(request.data.setdefault("ClockWise", False))
            .add_area_mode(request.data.setdefault("AreaMode", "constant"))
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_angle(serializer=serializer)
            .add_clock_wise(serializer=serializer)
            .add_area_mode(serializer=serializer)
        )

    def apply(self, *args, **kwargs):
        angle = self.angle
        if self.clock_wise:
            angle *= -1
        if self.add_area_mode == "constant":
            img = PIL.Image.fromarray(self.Image).rotate(
                angle, PIL.Image.BILINEAR, expand=True
            )
            self.Image = np.array(img)
        else:
            self.Image = rotate(
                self.Image, angle=angle, resize=True, mode=self.add_area_mode
            )
            self.Image = self.normalize8(self.Image)
        return self


class ResizeTool(PhotoTool):
    def __init__(self, width=720, high=480) -> None:
        self.width = width
        self.high = high

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_width(self, width=720, serializer=None):
        if serializer is not None:
            width = serializer.data["Width"]
        if type(width) == str and width == "":
            width = 720
        if type(width) != int:
            width = int(width)
        if width <= 25:
            width = 720
        self.width = width
        return self

    def add_high(self, high=480, serializer=None):
        if serializer is not None:
            high = serializer.data["High"]
        if type(high) == str and high == "":
            high = 480
        if type(high) != int:
            high = int(high)
        if high <= 25:
            high = 480
        self.high = high
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_high(request.data.setdefault("High", 480))
            .add_width(request.data.setdefault("Width", 720))
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_high(serializer=serializer)
            .add_width(serializer=serializer)
        )

    def apply(self, *args, **kwargs):
        self.Image = cv2.resize(
            self.Image, (self.high, self.width), interpolation=cv2.INTER_CUBIC
        )
        return self


class ContrastTool(PhotoTool):
    def __init__(self, contrast=0, brightness=0) -> None:
        self.contrast = contrast
        self.brightness = brightness

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_brightness(self, brightness=0, serializer=None):
        if serializer is not None:
            brightness = serializer.data["Brightness"]
        if type(brightness) == str and brightness == "":
            brightness = 0
        if type(brightness) != int:
            brightness = int(brightness)
        if brightness < -100 or brightness > 100:
            brightness = 0
        self.brightness = brightness
        return self

    def add_contrast(self, contrast=0, serializer=None):
        if serializer is not None:
            contrast = serializer.data["Contrast"]
        if type(contrast) == str and contrast == "":
            contrast = 0
        if type(contrast) != int:
            contrast = int(contrast)
        if contrast < -100 or contrast > 100:
            contrast = 0
        self.contrast = contrast
        return self

    def request2data(self, request):
        return (
            super()
            .request2data(request)
            .add_brightness(request.data.setdefault("Brightness",0))
            .add_contrast(request.data.setdefault("Contrast",50))
        )

    def serializer2data(self, serializer):
        return (
            super()
            .serializer2data(serializer)
            .add_brightness(serializer=serializer)
            .add_contrast(serializer=serializer)
        )

    def apply(self, *args, **kwargs):
        alpha = self.contrast / 50
        beta = int(self.brightness)
        self.Image = cv2.convertScaleAbs(self.Image, alpha=alpha, beta=beta)
        return self


class SaturationTool(PhotoTool):
    def __init__(self, saturation=0) -> None:
        self.saturation = saturation

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def add_saturation(self, saturation=0, serializer=None):
        if serializer is not None:
            saturation = serializer.data["Saturation"]
        if type(saturation) == str and saturation == "":
            saturation = 0
        if type(saturation) != int:
            saturation = int(saturation)
        if saturation < -100 or saturation > 100:
            saturation = 0
        self.saturation = saturation
        return self

    def serializer2data(self, serializer):
        return super().serializer2data(serializer).add_saturation(serializer=serializer)

    def apply(self, *args, **kwargs):
        from PIL import ImageEnhance

        image = PIL.Image.fromarray(self.Image)
        after_enh_image = ImageEnhance.Color(image).enhance(self.saturation / 50)
        self.Image = np.array(after_enh_image)
        return self

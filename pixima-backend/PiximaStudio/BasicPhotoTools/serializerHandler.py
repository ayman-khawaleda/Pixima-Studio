from AbstractSerializer.serializerHandler import ImageSerializerHandler
from . import serializer


class CropImageSerializerHandler(ImageSerializerHandler):
    def __init__(
        self,
        serializer: serializer.CropImageSerializer,
        preview_optinos: list = None,
        ratio_options: list = None,
    ) -> None:
        super().__init__(serializer, preview_optinos)
        if ratio_options is None:
            self.ratio_options = ["1:1", "4:3", "5:4", "9:16", "16:9"]

    def all_cords(self):
        return (
            True
            if (
                self.serializer.data["X1"] == -1
                and self.serializer.data["X2"] == -1
                and self.serializer.data["Y1"] == -1
                and self.serializer.data["Y2"] == -1
            )
            else False
        )

    def correct_sort_cords(self):
        cords = [
            self.serializer.data["X1"],
            self.serializer.data["X2"],
            self.serializer.data["Y1"],
            self.serializer.data["Y2"],
        ]
        for i, val in enumerate(cords):
            if val is None:
                return False
            if val < 0:
                cords[i] = 0
        return True if cords[0] < cords[1] and cords[2] < cords[3] else False

    def handle(self) -> bool:
        res = super().handle()
        if res:
            if self.all_cords() and self.serializer.data["Ratio"] is None:
                self.errors = {"Message": "Provide Either [X1,X2,Y1,Y2] Or Ratio"}
                return False
            if (
                self.serializer.data["Ratio"] not in self.ratio_options
                and self.serializer.data["Ratio"] is not None
            ):
                self.errors = {
                    "Message": f"Ratio Should Be One Of The Values {self.ratio_options}"
                }
                return False
            if not self.correct_sort_cords() and self.serializer.data["Ratio"] is None:
                self.errors = {"Message": "Error In [X1,X2,Y1,Y2] Values"}
                return False
        return res


class FlipImageSerializerHandler(ImageSerializerHandler):
    def __init__(
        self,
        serializer: serializer.ImageSerializer,
        preview_optinos: list = None,
        direction_options: list = None,
    ) -> None:
        super().__init__(serializer, preview_optinos)
        if direction_options is None:
            self.direction_options = ["Hor", "Ver"]

    def handle(self) -> bool:
        res = super().handle()
        if res:
            if self.serializer.data["Direction"] is None:
                self.errors = {"Message": "Direction Can't Be Empty"}
                return False
            if self.serializer.data["Direction"] not in self.direction_options:
                self.errors = {
                    "Message": f"Direction Should Be One of The Values {self.direction_options}"
                }
                return False
        return res


class RotateImageSerializerHandler(ImageSerializerHandler):
    def __init__(
        self,
        serializer: serializer.ImageSerializer,
        preview_optinos: list = None,
        area_mode: list = None,
    ) -> None:
        super().__init__(serializer, preview_optinos)
        if area_mode is None:
            area_mode = ["constant", "edge", "symmetric", "reflect", "wrap"]
        self.area_mode = area_mode

    def angle_range_check(self):
        angle = self.serializer.data["Angle"]
        if 0 > angle or angle > 360:
            return False
        return True

    def handle(self) -> bool:
        res = super().handle()
        if res:
            if (
                self.serializer.data["Angle"] is None
                or self.serializer.data["ClockWise"] is None
            ):
                self.errors = {"Message": "Angle And ClockWise Can't be Empty"}
                return False
            if not self.angle_range_check():
                self.errors = {"Message": "Angle Should Be In Rnage [0:360]"}
                return False
            if not self.serializer.data["AreaMode"] in self.area_mode:
                self.errors = {
                    "Message": f"AreaMode Should Be one Of The Values {self.area_mode}"
                }
                return False
        return res


class ResizeImageSerializerHandler(ImageSerializerHandler):
    def __init__(
        self,
        serializer: serializer.ImageSerializer,
        preview_optinos: list = None,
    ) -> None:
        super().__init__(serializer, preview_optinos)

    def handle(self) -> bool:
        res = super().handle()
        if res:
            if (
                self.serializer.data["Width"] is None
                or self.serializer.data["High"] is None
            ):
                self.errors = {"Message": "Width And High Can't be Empty"}
                return False
            if self.serializer.data["Width"] < 25 or self.serializer.data["High"] < 25:
                self.errors = {"Message": "Width And High Shouldn't Be Less Than 25px"}
                return False
        return res


class ContrastImageSerializerHandler(ImageSerializerHandler):
    def __init__(
        self,
        serializer: serializer.ImageSerializer,
        preview_optinos: list = None,
    ) -> None:
        super().__init__(serializer, preview_optinos)

    def check_contrast_range(self):
        contrast = self.serializer.data["Contrast"]
        if 0 > contrast or contrast > 100:
            return False
        return True

    def check_brightness_range(self):
        brightness = self.serializer.data["Brightness"]
        if -100 > brightness or brightness > 100:
            return False
        return True

    def handle(self) -> bool:
        res = super().handle()
        if res:
            if (
                self.serializer.data["Contrast"] is None
                or self.serializer.data["Brightness"] is None
            ):
                self.errors = {"Message": "Contrast And Brightness Can't be Empty"}
                return False
            if not self.check_contrast_range():
                self.errors = {"Message": "Contrast Should Be In Range [0,100]"}
                return False
            if not self.check_brightness_range():
                self.errors = {"Message": "Brightness Should Be In Range [-100,100]"}
                return False
        return res


class SaturationImageSerializerHandler(ImageSerializerHandler):
    def __init__(
        self,
        serializer: serializer.ImageSerializer,
        preview_optinos: list = None,
    ) -> None:
        super().__init__(serializer, preview_optinos)

    def check_saturation_range(self):
        saturation = self.serializer.data["Saturation"]
        if 0 > saturation or saturation > 100:
            return False
        return True

    def handle(self) -> bool:
        res = super().handle()
        if res:
            if self.serializer.data["Saturation"] is None:
                self.errors = {"Message": "Saturation Can't be Empty"}
                return False
            if not self.check_saturation_range():
                self.errors = {"Message": "Saturation Should Be In Range [0,100]"}
                return False
        return res

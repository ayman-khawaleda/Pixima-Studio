from abc import abstractmethod, ABCMeta
from rest_framework.serializers import Serializer
from . import serializer
from Core.models import UploadImageModel
from PiximaStudio.settings import MEDIA_ROOT
import os


class SerializerHandler(metaclass=ABCMeta):
    def __init__(self, serializer: Serializer) -> None:
        self.serializer = serializer
        self.errors = {}

    @abstractmethod
    def handle(self) -> bool:
        pass


class ImageSerializerHandler(SerializerHandler):
    def __init__(
        self,
        serializer: serializer.ImageHandlerSerializer,
        preview_optinos: list = None,
    ) -> None:
        super().__init__(serializer)
        if preview_optinos is None:
            self.preview_options = ["None", "Low", "Mid", "High"]

    def __image_index_exists(self):
        directory_id = self.serializer.data["id"]
        index = self.serializer.data["ImageIndex"]
        return (
            True
            if os.path.exists(
                os.path.join(
                    MEDIA_ROOT, "Images", str(directory_id), str(index) + ".jpg"
                )
            )
            else False
        )

    def handle(self) -> bool:
        res = self.serializer.is_valid()
        if res:
            if (
                self.serializer.data["id"] is None
                and self.serializer.data["Image"] is None
            ):
                self.errors = {"Message": "Both id and Image Can't Be Null"}
                return False
            if self.serializer.data["ImageIndex"] < 0:
                self.errors = {"Message": "ImageIndex Less Than 0"}
                return False
            if not self.__image_index_exists() and self.serializer.data["id"]:
                self.errors = {"Message": "ImageIndex Not Found"}
                return False
            if self.serializer.data["Preview"] not in self.preview_options:
                self.errors = {
                    "Message": f"Preview Should Be On Of This Values {self.preview_options}"
                }
                return False
            try:
                query_set = UploadImageModel.objects.get(id=self.serializer.data["id"])
                if not query_set:
                    raise UploadImageModel.DoesNotExist()
            except UploadImageModel.DoesNotExist as ex:
                self.errors = {"Message": "Id Not Found"}
                return False
        if not res:
            self.errors = self.serializer.errors
        return res


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
        serializer: serializer.ImageHandlerSerializer,
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
        serializer: serializer.ImageHandlerSerializer,
        preview_optinos: list = None,
        area_mode:list = None
    ) -> None:
        super().__init__(serializer, preview_optinos)
        if area_mode is None:
            area_mode = ['constant', 'edge', 'symmetric', 'reflect', 'wrap']
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
                self.errors = {"Message": f"AreaMode Should Be one Of The Values {self.area_mode}"}
                return False                
        return res

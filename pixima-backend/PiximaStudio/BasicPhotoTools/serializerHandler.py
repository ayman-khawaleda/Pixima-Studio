from abc import abstractmethod, ABCMeta
from rest_framework.serializers import Serializer
from . import serializer
from Core.models import UploadImageModel


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
            if self.serializer.data["Preview"] not in self.preview_options:
                self.errors = {
                    "Message": "Preview Should Be On Of This Value ['None', 'Low', 'Mid', 'High']"
                }
                return False
            try:
                query_set = UploadImageModel.objects.get(
                    id=self.serializer.data["id"]
                )
                if not query_set:
                    raise UploadImageModel.DoesNotExist()
            except UploadImageModel.DoesNotExist as ex:
                self.errors = {"Message": "Id Not Found"}
                return False
        if not res:
            self.errors = self.serializer.errors
        return res

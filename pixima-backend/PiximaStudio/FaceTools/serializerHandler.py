from AbstractSerializer.serializerHandler import ImageSerializerHandler
from . import serializer


class EyesColorSerializerHandler(ImageSerializerHandler):
    def handle(self) -> bool:
        return super().handle()


class EyesResizeSerializerHandler(ImageSerializerHandler):
    def handle(self) -> bool:
        return super().handle()


class NoseResizeSerializerHandler(ImageSerializerHandler):
    def handle(self) -> bool:
        return super().handle()


class CleatFaceBlurSerializerHandler(ImageSerializerHandler):
    def __init__(
        self,
        serializer: serializer.ImageSerializer,
        preview_optinos: list = None,
        method_list: list = None,
    ) -> None:
        super().__init__(serializer, preview_optinos)
        if method_list is None:
            method_list = ["GaB", "BiB"]
        self.method_list = method_list

    def handle(self) -> bool:
        res = super().handle()
        if res:
            method = self.serializer.data["Method"]
            if not method in self.method_list:
                self.errors = {
                    "Message": f"Method Should Be One Of These Values {self.method_list}"
                }
                return False
        else:
            self.errors = self.serializer.errors
        return res

from AbstractSerializer import serializer, serializerHandler


class GlitchFilterSerializerHandler(serializerHandler.ImageSerializerHandler):
    def __init__(
        self, serializer: serializer.ImageSerializer, preview_optinos: list = None
    ) -> None:
        super().__init__(serializer, preview_optinos)

    def handle(self) -> bool:
        res = super().handle()
        if res:
            shift = self.serializer.data["Shift"]
            if shift > 50 or shift < 5:
                self.errors = {"Message": "Shift Should Be In Range [5, 50]"}
                return False

            step = self.serializer.data["Step"]
            if step > 25 or step < 5:
                self.errors = {"Message": "Step Should Be In Range [5, 25]"}
                return False

            density = self.serializer.data["Density"]
            if density > 50 or density < 0:
                self.errors = {"Message": "Density Should Be In Range [0, 50]"}
                return False
        if not res:
            self.errors = self.serializer.errors
        return res


class CirclesFilterSerializerHandler(serializerHandler.ImageSerializerHandler):
    def __init__(
        self,
        serializer: serializer.ImageSerializer,
        preview_optinos: list = None,
        facekey_options: list = None,
    ) -> None:
        super().__init__(serializer, preview_optinos)
        self.facekey_options = facekey_options
        if facekey_options is None:
            self.facekey_options = ["RightEye", "LeftEye", "Nose"]

    def handle(self) -> bool:
        res = super().handle()
        if res:
            x, y, face_key, radius = (
                self.serializer.data["X"],
                self.serializer.data["Y"],
                self.serializer.data["FaceKey"],
                self.serializer.data["Radius"],
            )
            if face_key == "None" and (x <= -1 or y <= -1):
                self.errors = {
                    "Message": f"You Have To Provide Either FaceKey Values {self.facekey_options} or [X, Y]"
                }
                return False

            if (x >= 0 and y < -1) or (x < -1 and y >= 0):
                self.errors = {"Message": "Please Provide Valid [X, Y]"}
                return False

            if face_key not in [*self.facekey_options, "None"]:
                self.errors = {
                    "Message": f"The FaceKey Should Be One Of The Values {self.facekey_options}"
                }
                return False

            if radius > 30 or radius < 5:
                self.errors = {"Message": "Radius Should Be In Range [5, 30]"}
                return False
        if not res:
            self.errors = self.serializer.errors
        return res

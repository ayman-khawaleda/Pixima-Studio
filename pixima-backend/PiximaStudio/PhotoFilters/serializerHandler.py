from AbstractSerializer import serializer,serializerHandler

class GlitchFilterSerializerHandler(serializerHandler.ImageSerializerHandler):
    def __init__(self, serializer: serializer.ImageSerializer, preview_optinos: list = None) -> None:
        super().__init__(serializer, preview_optinos)
    
    def handle(self) -> bool:
        res = super().handle()
        if res:
            shift = self.serializer.data["Shift"]
            if shift > 50 or shift < 5:
                self.errors = {"Message":"Shift Should Be In Range [5, 50]"}
                return False
            
            step = self.serializer.data["Step"]
            if step > 25 or step < 5:
                self.errors = {"Message":"Step Should Be In Range [5, 25]"}
                return False
            
            density = self.serializer.data["Density"]
            if density > 50 or density < 0:
                self.errors = {"Message":"Density Should Be In Range [0, 50]"}
                return False
        if not res:
            self.errors = self.serializer.errors
        return res
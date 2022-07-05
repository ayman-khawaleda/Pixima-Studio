from abc import abstractmethod
from PiximaTools.abstractTools import Tool


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
                serializer.data["X1"],
                serializer.data["X2"],
                serializer.data["Y1"],
                serializer.data["Y2"],
            )
        self.cords = [X1, X2, Y1, Y2]
        return self

    def check_cords(self):
        if self.cords is None:
            return False
        if any([x <= -1 for x in self.cords]):
            return False
        return True

    def add_ratio(self, ratio: str=None,serializer=None):
        if serializer is not None:
            ratio = serializer.data["Ratio"]
        self.ratio = ratio
        return self

    def serializer2data(self, serializer):
        return super()\
            .serializer2data(serializer)\
                .add_cords(serializer=serializer)\
                    .add_ratio(serializer=serializer)

    def apply(self, *args, **kwargs):
        if self.check_cords():
            print("Cords: ", self.cords)
        else:
            print("Ratio: ", self.ratio)
        print(self.Image.shape)
        return self

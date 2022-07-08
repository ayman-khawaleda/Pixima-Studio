from abc import abstractmethod
from PiximaTools.abstractTools import Tool


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
        if shift > 50 or shift < 5:
            shift = 20
        self.shift = shift
        return self

    def add_step(self, step=15, serializer=None):
        if serializer is not None:
            step = serializer.data["Step"]
        if step > 25 or step < 5:
            step = 20
        self.step = step
        return self

    def add_density(self, density=5, serializer=None):
        if serializer is not None:
            density = serializer.data["Density"]
        if density > 50 or density < 0:
            density = 5
        self.density = density
        return self

    def apply(self, *args, **kwargs):
        return self

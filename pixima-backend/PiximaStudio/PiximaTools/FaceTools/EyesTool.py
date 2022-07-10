from abc import abstractmethod, ABC
from .FaceTools import FaceTool

class EyesTool(FaceTool):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass


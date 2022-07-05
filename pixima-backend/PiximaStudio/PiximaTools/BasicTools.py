from abc import abstractmethod
from PiximaTools.abstractTools import Tool

class PhotoTool(Tool):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass


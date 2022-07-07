from abc import abstractmethod
from PiximaTools.abstractTools import Tool

class Filter(Tool):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass        


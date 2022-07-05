from abc import abstractmethod
from PiximaTools.abstractTools import Tool

class PhotoTool(Tool):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

class CropTool(PhotoTool):
    def __init__(self,cords:list=None,ratio:str='1:1') -> None:
        self.cords = cords
        self.ratio = ratio

    def __call__(self, *args, **kwargs):
        return self.apply(*args,**kwargs)

    def add_cords(self,X1,X2,Y1,Y2):
        self.cords = [X1,X2,Y1,Y2]
        return self
    
    def add_ratio(self,ratio:str):
        self.ratio = ratio
        return self

    def apply(self,*args,**kwargs):
        return self

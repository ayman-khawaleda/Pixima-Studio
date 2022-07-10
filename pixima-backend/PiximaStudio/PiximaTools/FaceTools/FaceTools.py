from abc import abstractmethod, ABC
from PiximaTools.abstractTools import Tool
from PiximaStudio.settings import MEDIA_ROOT, MEDIA_URL
from skimage import io
from PiximaTools.Exceptions import ImageNotSaved
import os


class FaceTool(Tool, ABC):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

    def save_mask(self, *args, **kwargs):
        if "quality" in kwargs.keys():
            quality = kwargs["quality"]
        else:
            quality = 90
        try:
            sub_path = os.path.join(MEDIA_ROOT, "ImageMasks", str(self.directory_id))
            if not os.path.exists(sub_path):
                os.mkdir(sub_path)
            self.lastidx = len(os.listdir(sub_path))
            full_path = os.path.join(sub_path, f"{self.lastidx}.jpg")
            io.imsave(full_path, self.Mask, quality=quality)
            mask_path = os.path.join(
                MEDIA_URL, "ImageMasks", str(self.directory_id), f"{self.lastidx}.jpg"
            )
            return mask_path
        except Exception as e:
            raise ImageNotSaved("Error In Save Image Mask")

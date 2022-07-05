from abc import ABC, abstractmethod
import math
from PiximaStudio.settings import MEDIA_ROOT
from skimage.io import imsave, imread
import os

class Tool(ABC):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

    def add_id(self, id):
        self.directory_id = id
        return self

    def add_image(self, img):
        self.Image = img
        return self

    def read_image(self, image_index: int = 0, path=None):
        if self.directory_id is None:
            raise Exception("Need Directory id")
        try:
            if path is not None:
                self.Image = imread(path)
            else:
                path = os.path.join(
                    MEDIA_ROOT, "Images", str(self.directory_id), f"{image_index}.jpg"
                )
                self.Image = imread(path)
            return True
        except Exception as e:
            print(e)
            return False

    def save_image(self, *argm, **kwargs):
        if "id" in kwargs.keys():
            self.directory_id = kwargs["id"]
        try:
            sub_path = os.path.join(MEDIA_ROOT, "Images", str(self.directory_id))
            lastidx = len(os.listdir(sub_path))
            imsave(os.path.join(sub_path, f"{lastidx}.jpg"), self.Image)
            return True
        except Exception as e:
            print(e)
            return False

    def normaliz_pixel(self, normalized_x, normalized_y, image_width, image_height):
        def is_valid_normalized_value(value: float):
            return (value > 0 or math.isclose(0, value)) and (
                value < 1 or math.isclose(1, value)
            )

        if not (
            is_valid_normalized_value(normalized_x)
            and is_valid_normalized_value(normalized_y)
        ):
            return None

        x_px = min(math.floor(normalized_x * image_width), image_width - 1)
        y_px = min(math.floor(normalized_y * image_height), image_height - 1)
        return x_px, y_px

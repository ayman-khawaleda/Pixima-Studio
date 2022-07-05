from abc import ABC, abstractmethod
import math
from PiximaStudio.settings import MEDIA_ROOT, MEDIA_URL
from skimage.io import imsave, imread
import os


class Tool(ABC):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

    def serializer2data(self, serializer):
        self.add_id(serializer.data["id"]).add_image_index(
            serializer.data["ImageIndex"]
        )
        return self

    def add_id(self, id):
        self.directory_id = id
        return self

    def add_image(self, img):
        self.Image = img
        return self

    def add_image_index(self, index):
        self.image_index = index
        return self

    def read_image(self, image_index: int = -1, path=None):
        if self.directory_id is None:
            raise Exception("Need Directory id")
        try:
            if path is not None:
                img_path = path
            elif image_index != -1:
                img_path = os.path.join(
                    MEDIA_ROOT, "Images", str(self.directory_id), f"{image_index}.jpg"
                )
            else:
                img_path = os.path.join(
                    MEDIA_ROOT,
                    "Images",
                    str(self.directory_id),
                    f"{self.image_index}.jpg",
                )
            self.Image = imread(img_path)
            return self
        except Exception as e:
            raise Exception("Error In Loading Image")

    def save_image(self, *args, **kwargs):
        if "id" in kwargs.keys():
            self.directory_id = kwargs["id"]
        if "quality" in kwargs.keys():
            self.quality = kwargs["quality"]
        else:
            self.quality = 90
        try:
            sub_path = os.path.join(MEDIA_ROOT, "Images", str(self.directory_id))
            lastidx = len(os.listdir(sub_path))
            full_path = os.path.join(sub_path, f"{lastidx}.jpg")
            imsave(full_path, self.Image, quality=self.quality)
            image_path = os.path.join(
                MEDIA_URL, "Images", str(self.directory_id), f"{lastidx}.jpg"
            )
            return image_path
        except Exception as e:
            raise Exception("Error In Saving Image")

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

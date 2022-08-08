from abc import ABC, abstractmethod
from PiximaStudio.settings import MEDIA_ROOT, MEDIA_URL, PROJECT_DIR
from skimage.io import imsave, imread
from PIL import Image
from uuid import uuid4
from . import Exceptions
from Core.models import ImageOperationsModel
from PiximaTools.Exceptions import ImageNotSaved
import os
import cv2
import math
import numpy as np


class Tool(ABC):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

    def add_quality_dict(self, quality_dict: dict = {"High": 70, "Mid": 40, "Low": 15}):
        self.quality = quality_dict
        return self

    def file2image(self, file):
        img = Image.open(file)
        self.Image = np.array(img)
        self.add_id(uuid4())
        return self

    def request2data(self, request):
        file = request.data["Image"].file
        self.file2image(file).add_quality_dict().add_preview(
            request.data.setdefault("Preview", "None")
        )
        return self

    def serializer2data(self, serializer):
        self.add_id(serializer.data["id"]).add_image_index(
            serializer.data["ImageIndex"]
        ).add_preview(serializer.data["Preview"]).add_quality_dict()
        return self

    def add_preview(self, preview):
        self.preview = preview
        return self

    def add_id(self, id):
        self.directory_id = id
        return self

    def add_image(self, img):
        self.Image = img
        return self

    def add_image_index(self, index):
        if index == -1:
            path = os.path.join(
                PROJECT_DIR, MEDIA_ROOT, "Images", str(self.directory_id)
            )
            ImagesPath = os.listdir(path)
            ImageOrderPath = []
            for path in ImagesPath:
                sub_path = path.split(f"{os.path.sep}")[-1]
                number = sub_path.split(".")[0]
                ImageOrderPath.append((int(number),path))
            ImageOrderPath = sorted(ImageOrderPath,key=lambda x:x[0])
            index = ImageOrderPath[-1][0]
        self.image_index = index
        return self

    def read_image(self, image_index: int = -1, path=None):
        if self.directory_id is None:
            raise Exceptions.NeedDirectoryID("Need Directory id")
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
            raise Exceptions.ImageNotFound("Error In Loading Image")

    def save_image(self, *args, **kwargs):
        if "id" in kwargs.keys():
            self.directory_id = kwargs["id"]
        if "quality" in kwargs.keys():
            quality = kwargs["quality"]
        else:
            quality = 100
        try:
            sub_path = os.path.join(MEDIA_ROOT, "Images", str(self.directory_id))
            if not os.path.exists(sub_path):
                os.mkdir(sub_path)
            self.lastidx = ImageOperationsModel.objects.filter(image=str(self.directory_id)).count()+1
            full_path = os.path.join(sub_path, f"{self.lastidx}.jpg")
            imsave(full_path, self.Image, quality=quality)
            image_path = os.path.join(
                MEDIA_URL, "Images", str(self.directory_id), f"{self.lastidx}.jpg"
            )
            return image_path
        except Exception as e:
            raise Exceptions.ImageNotSaved("Error In Saving Image")

    def get_preview(self):
        quality = self.quality["High"]
        if self.preview == "Low":
            quality = self.quality["Low"]
        elif self.preview == "Mid":
            quality = self.quality["Mid"]

        if quality == 90:
            return os.path.join(
                MEDIA_URL, "Images", str(self.directory_id), f"{self.lastidx}.jpg"
            )
        if self.lastidx is None:
            raise Exceptions.ImageIndexNotFound("Please Call Save Image First!!")

        dir_path = os.path.join(MEDIA_ROOT, "Temp", str(self.directory_id))
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        image_path = os.path.join(
            MEDIA_ROOT,
            "Temp",
            str(self.directory_id),
            f"{self.lastidx}_{self.preview}.jpg",
        )
        try:
            Image.fromarray(self.Image).save(image_path, optimize=True, quality=quality)
            return os.path.join(
                MEDIA_URL,
                "Temp",
                str(self.directory_id),
                f"{self.lastidx}_{self.preview}.jpg",
            )
        except Exception as e:
            raise Exceptions.ImageNotSaved("Error While Saving Preview Image")

    def normalize8(self, I):
        mn = I.min()
        mx = I.max()
        mx -= mn
        I = ((I - mn) / mx) * 255
        return I.astype(np.uint8)

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


class BodyTool(Tool, ABC):
    @classmethod
    @abstractmethod
    def apply(self, *args, **kwargs):
        pass

    def save_mask(self, *args, **kwargs):
        try:
            sub_path = os.path.join(MEDIA_ROOT, "ImageMasks", str(self.directory_id))
            if not os.path.exists(sub_path):
                os.mkdir(sub_path)
            self.lastidx = len(os.listdir(sub_path))
            full_path = os.path.join(sub_path, f"{self.lastidx}.jpg")
            cv2.imwrite(full_path, self.Mask)
            mask_path = os.path.join(
                MEDIA_URL, "ImageMasks", str(self.directory_id), f"{self.lastidx}.jpg"
            )
            return mask_path
        except Exception as e:
            raise ImageNotSaved("Error In Save Image Mask")

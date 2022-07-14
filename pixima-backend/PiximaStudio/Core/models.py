from uuid import uuid4
from django.db import models
import os

# Model For Upload Images


def upload_to(ins, filename):
    return f'{os.path.join("Images",str(ins.id),"0."+filename.split(".")[-1])}'


class ImageModel(models.Model):
    class Meta:
        db_table = "images"
        ordering = ("upload_time",)

    id = models.UUIDField(
        default=uuid4, primary_key=True, unique=True, db_index=True, editable=False
    )
    Image = models.ImageField(upload_to=upload_to)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)


class ImageOperationsManager(models.Manager):
    def create(self, **kwargs):
        try:
            query = ImageOperationsModel.objects.filter(image_id=str(kwargs["image"]))
            kwargs["operation_num"] = query.count() + 1
            return super().create(**kwargs)
        except Exception as e:
            return super().create(**kwargs)


class ImageOperationsModel(models.Model):
    objects = ImageOperationsManager()

    class Meta:
        db_table = "image_operations"
        ordering = ("operation_num",)

    image = models.ForeignKey(
        ImageModel,
        related_name="ImageOperations",
        on_delete=models.CASCADE,
        default=None,
    )
    operation_num = models.IntegerField(default=0, blank=True, null=True)
    operation_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.operation_name + " Id: " + str(self.image.id)

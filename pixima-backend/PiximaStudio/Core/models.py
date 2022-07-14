from uuid import uuid4
from django.db import models
import os

# Model For Upload Images


def upload_to(ins, filename):
    return f'{os.path.join("Images",str(ins.id),"0."+filename.split(".")[-1])}'

class ImageModel(models.Model):
    class Meta:
        db_table = "uploaded_image"
        ordering = ("upload_time",)

    id = models.UUIDField(
        default=uuid4, primary_key=True, unique=True, db_index=True, editable=False
    )
    Image = models.ImageField(upload_to=upload_to)
    upload_time = models.DateTimeField(auto_now_add=True)
from uuid import uuid4
from django.db import models
import os
#Model For Upload Images

def upload_to(ins,filename):
    return f'{os.path.join("Images",str(uuid4())+"."+filename.split(".")[-1])}'

class UploadImageModel(models.Model):
    class Meta:
        db_table = 'uploaded_image'
    Image = models.ImageField(upload_to=upload_to)
    upload_time = models.DateTimeField(auto_now_add=True)
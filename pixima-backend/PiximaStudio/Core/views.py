from django.shortcuts import render
from django.views import View
from rest_framework.parsers import MultiPartParser, FormParser
from . import serializers
from PiximaStudio.settings import MEDIA_ROOT, PROJECT_DIR, MEDIA_URL
from PiximaStudio.AbstractView import RESTView
import os

# Create your views here.


class Index(View):
    template_name = "index.html"

    def get(self, request):
        context = {}
        return render(
            request=request, template_name=self.template_name, context=context
        )


class UploadImage(RESTView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        image_serializer = serializers.UploadImageSerializer(data=request.data)
        if image_serializer.is_valid():
            ins = image_serializer.save()
            return self.ok_request(
                {
                    "id": str(ins.id),
                    **image_serializer.data,
                }
            )
        return self.bad_request(image_serializer.errors)


class ImagesDirectoryId(RESTView):

    parser_classes = [MultiPartParser, FormParser]

    def delete(self, request, format=None):
        delete_serializer = serializers.DeleteImageSerializer(data=request.data)

        if delete_serializer.is_valid():
            path = os.path.join(
                PROJECT_DIR, MEDIA_ROOT, "Images", delete_serializer["id"].value
            )
            if os.path.exists(path):
                ImagesPaths = [
                    (int(x.split(".")[0]), x.split(".")[1]) for x in os.listdir(path)
                ]
                ImagesPaths = sorted(ImagesPaths, key=lambda x: x[0])
                ImagesPaths = [str(num) + "." + suffix for num, suffix in ImagesPaths]
                if len(ImagesPaths) == 1:
                    return self.ok_request(
                        {
                            "id": str(delete_serializer["id"].value),
                            "Image": os.path.join(
                                MEDIA_URL,
                                "Images",
                                delete_serializer["id"].value,
                                ImagesPaths[0],
                            ),
                        }
                    )
                else:
                    removed_image_path = os.path.join(
                        PROJECT_DIR,
                        MEDIA_ROOT,
                        "Images",
                        delete_serializer["id"].value,
                        ImagesPaths[-1],
                    )
                    image_path = os.path.join(
                        MEDIA_URL,
                        "Images",
                        delete_serializer["id"].value,
                        ImagesPaths[-2],
                    )
                    os.remove(removed_image_path)
                    return self.ok_request(
                        {
                            "id": str(delete_serializer["id"].value),
                            "Image": image_path,
                        },
                    )
            else:
                return self.bad_request({"id": ["NOT FOUND"]})

    def get(self, request, format=None):
        id_serializer = serializers.GetImageSerializer(data=request.query_params)
        if id_serializer.is_valid():
            path = os.path.join(
                PROJECT_DIR, MEDIA_ROOT, "Images", id_serializer["id"].value
            )
            if os.path.exists(path):
                numbers = [
                    (int(x.split(".")[0]), x.split(".")[1]) for x in os.listdir(path)
                ]
                numbers = sorted(numbers, key=lambda x: x[0])
                numbers = [str(num) + "." + suffix for num, suffix in numbers]

                return self.ok_request(
                    {
                        "id": str(id_serializer["id"].value),
                        "images": {
                            i: os.path.join(
                                MEDIA_URL, "Images", id_serializer["id"].value, x
                            )
                            for i, x in enumerate(numbers)
                        },
                    }
                )
            else:
                return self.bad_request({"id": ["NOT FOUND"]})
        return self.bad_request(id_serializer.errors)

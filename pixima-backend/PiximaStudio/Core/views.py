from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from . import serializers, models
from PiximaStudio.settings import MEDIA_ROOT, PROJECT_DIR, MEDIA_URL
import os

# Create your views here.


class Index(View):
    template_name = "index.html"

    def get(self, request):
        context = {}
        return render(
            request=request, template_name=self.template_name, context=context
        )


class UploadImage(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        image_serializer = serializers.UploadImageSerializer(data=request.data)
        if image_serializer.is_valid():
            ins = image_serializer.save()
            return JsonResponse(
                {
                    "code": HTTP_200_OK,
                    "status": "OK",
                    "id": str(ins.id),
                    **image_serializer.data,
                }
            )
        return JsonResponse(
            {
                "code": HTTP_400_BAD_REQUEST,
                "status": "BAD REQUEST",
                **image_serializer.errors,
            }
        )


class GetImagesDirectoryId(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        id_serializer = serializers.GetImageSerializer(data=request.data)
        if id_serializer.is_valid():
            path = os.path.join(
                PROJECT_DIR, MEDIA_ROOT, "Images", id_serializer["id"].value
            )
            if os.path.exists(path):
                numbers = [(int(x.split('.')[0]),x.split('.')[1]) for x in os.listdir(path)]
                numbers = sorted(numbers,key=lambda x: x[0])
                numbers = [str(num) + "." + suffix for num,suffix in numbers]

                return JsonResponse(
                    {
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "id": str(id_serializer["id"].value),
                        "images": {
                            i: os.path.join(
                                MEDIA_URL, "Images", id_serializer["id"].value, x
                            )
                            for i, x in enumerate(
                                numbers
                            )
                        },
                    }
                )
            else:
                return JsonResponse(
                    {
                        "code": HTTP_400_BAD_REQUEST,
                        "status": "BAD REQUEST",
                        "id": ["NOT FOUND"],
                    }
                )
        return JsonResponse(
            {
                "code": HTTP_400_BAD_REQUEST,
                "status": "BAD REQUEST",
                **id_serializer.errors,
            }
        )

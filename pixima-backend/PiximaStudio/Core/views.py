from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from . import serializers

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
            image_serializer.save()
            return JsonResponse(
                {"code": HTTP_200_OK, "status": "OK", **image_serializer.data}
            )
        return JsonResponse(
            {
                "code": HTTP_400_BAD_REQUEST,
                "status": "BAD REQUEST",
                **image_serializer.errors,
            }
        )

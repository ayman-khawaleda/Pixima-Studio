from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import JsonResponse
from .serializer import (
    ContrastImageSerializer,
    CropImageSerializer,
    FlipImageSerializer,
    ResizeImageSerializer,
    RotateImageSerializer,
)
from .serializerHandler import (
    ImageSerializerHandler,
    CropImageSerializerHandler,
    FlipImageSerializerHandler,
    ResizeImageSerializerHandler,
    RotateImageSerializerHandler,
)


def bad_request(errors: dict):
    return JsonResponse(
        data={"code": HTTP_400_BAD_REQUEST, "status": "BAD REQUEST", **errors}
    )


class CropToolView(APIView):
    def post(self, request, format=None):
        crop_serializer = CropImageSerializer(data=request.data)
        im_handler = CropImageSerializerHandler(crop_serializer)
        if im_handler.handle():
            return JsonResponse(
                data={"code": HTTP_200_OK, "status": "OK", **crop_serializer.data}
            )
        return bad_request(im_handler.errors)


class FlipToolView(APIView):
    def post(self, request, format=None):
        flip_serializer = FlipImageSerializer(data=request.data)
        im_handler = FlipImageSerializerHandler(flip_serializer)
        if im_handler.handle():
            return JsonResponse(
                data={"code": HTTP_200_OK, "status": "OK", **flip_serializer.data}
            )
        return bad_request(im_handler.errors)


class RotateToolView(APIView):
    def post(self, request, format=None):
        rotate_serializer = RotateImageSerializer(data=request.data)
        im_handler = RotateImageSerializerHandler(rotate_serializer)
        if im_handler.handle():
            return JsonResponse(
                data={"code": HTTP_200_OK, "status": "OK", **rotate_serializer.data}
            )
        return bad_request(im_handler.errors)


class ResizeToolView(APIView):
    def post(self, request, format=None):
        resize_serializer = ResizeImageSerializer(data=request.data)
        im_handler = ResizeImageSerializerHandler(resize_serializer)
        if im_handler.handle():
            return JsonResponse(
                data={"code": HTTP_200_OK, "status": "OK", **resize_serializer.data}
            )
        return bad_request(im_handler.errors)

class ContrastToolView(APIView):
    def post(self, request, format=None):
        contrast_serializer = ContrastImageSerializer(data=request.data)
        im_handler = ImageSerializerHandler(contrast_serializer)
        if im_handler.handle():
            return JsonResponse(
                data={"code": HTTP_200_OK, "status": "OK", **contrast_serializer.data}
            )
        return bad_request(im_handler.errors)

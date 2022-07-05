from django.forms import ImageField
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import JsonResponse
from .serializer import CropImageSerializer, FlipImageSerializer, RotateImageSerializer

from .serializerHandler import (
    ImageSerializerHandler,
    CropImageSerializerHandler,
    FlipImageSerializerHandler,
    RotateImageSerializerHandler,
)
from PiximaTools.BasicTools import CropTool, FlipTool, RotatTool


def bad_request(errors: dict):
    return JsonResponse(
        data={"code": HTTP_400_BAD_REQUEST, "status": "BAD REQUEST", **errors}
    )


class CropToolView(APIView):
    def post(self, request, format=None):
        crop_tool = CropTool()
        crop_serializer = CropImageSerializer(data=request.data)
        im_handler = CropImageSerializerHandler(crop_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                file = request.data["Image"].file
                crop_tool.file2image(file).add_quality_dict().add_preview(
                    request.data["Preview"]
                ).add_ratio(request.data["Ratio"]).add_cords(serializer=request).apply()
                image_path = crop_tool.save_image()
                imagepreview_path = crop_tool.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                image_path = (
                    crop_tool.serializer2data(serializer=crop_serializer)
                    .add_quality_dict()
                    .read_image()
                    .apply()
                    .save_image()
                )
                imagepreview_path = crop_tool.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return bad_request({"Message": "Error During Crop Process"})
        return bad_request(im_handler.errors)


class FlipToolView(APIView):
    def post(self, request, format=None):
        flip_tool = FlipTool()
        flip_serializer = FlipImageSerializer(data=request.data)
        im_handler = FlipImageSerializerHandler(flip_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                file = request.data["Image"].file
                flip_tool.file2image(file).add_quality_dict().add_preview(
                    request.data["Preview"]
                ).add_direction(request.data["Direction"]).apply()
                image_path = flip_tool.save_image()
                imagepreview_path = flip_tool.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                image_path = (
                    flip_tool.serializer2data(flip_serializer)
                    .add_quality_dict()
                    .read_image()()
                    .save_image()
                )
                imagepreview_path = flip_tool.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return bad_request({"Message": "Error During Flip Process"})
        return bad_request(im_handler.errors)


class RotateToolView(APIView):
    def post(self, request, format=None):
        rotate_tool = RotatTool()
        rotate_serializer = RotateImageSerializer(data=request.data)
        im_handler = RotateImageSerializerHandler(rotate_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                file = request.data["Image"].file
                rotate_tool.file2image(file)\
                .add_quality_dict()\
                .add_preview(request.data["Preview"])\
                .add_angle(request.data["Angle"])\
                .add_clock_wise(request.data["ClockWise"])\
                .add_area_mode(request.data["AreaMode"])\
                .apply()
                image_path = rotate_tool.save_image()
                imagepreview_path = rotate_tool.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                image_path = (
                    rotate_tool.serializer2data(rotate_serializer)
                    .add_quality_dict()
                    .read_image()()
                    .save_image()
                )
                imagepreview_path = rotate_tool.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return bad_request({"Message": "Error During Rotate Process"})

        return bad_request(im_handler.errors)

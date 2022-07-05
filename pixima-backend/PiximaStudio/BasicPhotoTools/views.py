from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import JsonResponse
from .serializer import CropImageSerializer
from .serializerHandler import ImageSerializerHandler, CropImageSerializerHandler
from PiximaTools.BasicTools import CropTool


def bad_request(errors: dict):
    return JsonResponse(
        data={"code": HTTP_400_BAD_REQUEST, "status": "BAD REQUEST", **errors}
    )


class CropToolView(APIView):
    def post(self, request, format=None):
        crop_serializer = CropImageSerializer(data=request.data)
        im_handler = CropImageSerializerHandler(crop_serializer)
        if im_handler.handle():
            crop_tool = CropTool()
            try:
                image_path = (
                    crop_tool.serializer2data(serializer=crop_serializer)
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

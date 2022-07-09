from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import JsonResponse
from . import serializer, serializerHandler
from PiximaTools import Filters


def bad_request(errors: dict):
    return JsonResponse(
        data={"code": HTTP_400_BAD_REQUEST, "status": "BAD REQUEST", **errors}
    )


class GlitchFilterView(APIView):
    def post(self, request, format=None):
        glitch_filter = Filters.GlitchFilter()
        glicth_serializer = serializer.GlitchFilterSerializer(data=request.data)
        filter_handler = serializerHandler.GlitchFilterSerializerHandler(
            glicth_serializer
        )
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                glitch_filter.request2data(request=request)()
                image_path = glitch_filter.save_image()
                imagepreview_path = glitch_filter.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if filter_handler.handle():
                image_path = (
                    glitch_filter.serializer2data(glicth_serializer)
                    .read_image()()
                    .save_image()
                )
                imagepreview_path = glitch_filter.get_preview()

                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return bad_request({"Message": "Error In Glitch Filter Request"})
        return bad_request(filter_handler.errors)


class CircleFilterView(APIView):
    def post(self, request, format=None):
        circles_filter = Filters.CirclesFilter()
        circles_serializer = serializer.CirclesFilterSerializer(data=request.data)
        filter_handler = serializerHandler.CirclesFilterSerializerHandler(
            circles_serializer
        )
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                file = request.data["Image"].file
                circles_filter.request2data(request=request)()
                image_path = circles_filter.save_image()
                imagepreview_path = circles_filter.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if filter_handler.handle():
                circles_filter.serializer2data(
                    serializer=circles_serializer
                ).read_image().apply()
                image_path = circles_filter.save_image()
                imagepreview_path = circles_filter.get_preview()
                return JsonResponse(
                    data={
                        "code": HTTP_200_OK,
                        "status": "OK",
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return bad_request({"Message": "Error In Circles Filter Request"})
        return bad_request(filter_handler.errors)

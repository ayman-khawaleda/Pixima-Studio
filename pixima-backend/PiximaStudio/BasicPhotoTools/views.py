from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.http import JsonResponse
from .serializer import CropImageSerializer


def bad_request(errors:dict):
    return JsonResponse(
            data={
                "code": HTTP_400_BAD_REQUEST,
                "status": "BAD REQUEST",
                **errors
            }
        )
        
class CropToolView(APIView):

    def post(self,request,format=None):
        crop_serializer = CropImageSerializer(data=request.data)
        if crop_serializer.is_valid():
            return JsonResponse(
                data={
                    "code": HTTP_200_OK,
                    "status": "OK",
                    **crop_serializer.data
                }
            )
        return bad_request(crop_serializer.errors)

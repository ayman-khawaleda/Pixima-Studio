from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.http import JsonResponse
from .serializer import CropImageSerializer

class CropToolView(APIView):

    def post(self,request,format=None):
        crop_serializer = CropImageSerializer(data=request.data)
        if crop_serializer.is_valid():
            print(crop_serializer.data)
            return JsonResponse(
                data={
                    "code": HTTP_200_OK,
                    "status": "OK",
                    **crop_serializer.data
                }
            )
        return JsonResponse(
            data={
                "code": HTTP_400_BAD_REQUEST,
                "status": "BAD REQUEST",
                **crop_serializer.errors
            }
        )

from django.views import View
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import JsonResponse


class AbstractView(View):

    def bad_request(self,errors: dict):
        return JsonResponse(
            data={"code": HTTP_400_BAD_REQUEST, "status": "BAD REQUEST", **errors}
        )

    def ok_request(self,info: dict):
        return JsonResponse(data={"code": HTTP_200_OK, "status": "OK", **info})

class RESTView(AbstractView,APIView):
    pass
from rest_framework.views import APIView
from PiximaStudio.AbstractView import RESTView
from .serializer import EyesColorSerializer
from .serializerHandler import EyesColorSerializerHandler


class EyesColorToolView(RESTView):
    def post(self, request, format=None):
        eyescolor_serializer = EyesColorSerializer(data=request.data)
        eyescolor_serializerhandler = EyesColorSerializerHandler(eyescolor_serializer)
        try:
            if eyescolor_serializerhandler.handle():
                return self.ok_request(eyescolor_serializerhandler.serializer.data)
        except Exception as e:
            return self.bad_request({"Message": "Error During Flip Process"})
        return self.bad_request(eyescolor_serializerhandler.errors)

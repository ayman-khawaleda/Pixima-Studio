from django.shortcuts import render
from PiximaStudio.AbstractView import RESTView
from .serializer import ColorHairSerializer
from .serializerHandler import ColorHairSerializerHandler
from PiximaTools.Exceptions import RequiredValue,NoFace

class ColorHairToolView(RESTView):
    def post(self, request, format=None):
        colorhair_serializer = ColorHairSerializer(data=request.data)
        colorhair_serializerhandler = ColorHairSerializerHandler(
            colorhair_serializer
        )
        try:
            if colorhair_serializerhandler.handle():
                return self.ok_request(colorhair_serializer.data)
        except RequiredValue as e:
            return self.bad_request({"Message": str(e)})
        except NoFace as e:
            return self.bad_request({"Message": str(e)})
        except Exception as e:
            return self.bad_request({"Message": "Error During Hair Coloring Process"})
        return self.bad_request(colorhair_serializerhandler.errors)

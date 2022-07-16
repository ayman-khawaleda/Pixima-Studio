from django.shortcuts import render
from PiximaStudio.AbstractView import RESTView
from .serializer import ColorHairSerializer
from .serializerHandler import ColorHairSerializerHandler
from PiximaTools.Exceptions import RequiredValue, NoFace
from PiximaTools.BodyTools import HairTool
from Core.models import ImageModel,ImageOperationsModel

class ColorHairToolView(RESTView):
    def post(self, request, format=None):
        hair_tool = HairTool.ColorHairTool()
        colorhair_serializer = ColorHairSerializer(data=request.data)
        colorhair_serializerhandler = ColorHairSerializerHandler(colorhair_serializer)
        try:
            if colorhair_serializerhandler.handle():
                hair_tool.serializer2data(colorhair_serializer).read_image().apply()
                image_path = hair_tool.save_image()
                imagepreview_path = hair_tool.get_preview()
                mask_path = hair_tool.save_mask()
                ImageObj = ImageModel.objects.get(id=colorhair_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="ColorHairTool"
                ).save()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                        "Mask": mask_path,
                    }
                )
        except RequiredValue as e:
            return self.bad_request({"Message": str(e)})
        except NoFace as e:
            return self.bad_request({"Message": str(e)})
        except Exception as e:
            return self.bad_request({"Message": "Error During Hair Coloring Process"})
        return self.bad_request(colorhair_serializerhandler.errors)

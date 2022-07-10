from rest_framework.views import APIView
from PiximaStudio.AbstractView import RESTView
from .serializer import EyesColorSerializer
from .serializerHandler import EyesColorSerializerHandler
from PiximaTools.FaceTools import EyesTool
from PiximaTools.Exceptions import RequiredValue, NoFace


class EyesColorToolView(RESTView):
    def post(self, request, format=None):
        eyescolor_tool = EyesTool.EyesColorTool()
        eyescolor_serializer = EyesColorSerializer(data=request.data)
        eyescolor_serializerhandler = EyesColorSerializerHandler(eyescolor_serializer)
        try:
            if eyescolor_serializerhandler.handle():
                eyescolor_tool.serializer2data(eyescolor_serializer).read_image().apply()
                image_path = eyescolor_tool.save_image()
                imagepreview_path = eyescolor_tool.get_preview()
                mask_path = eyescolor_tool.save_mask()
                return self.ok_request({
                    "Image": image_path,
                    "ImagePreview": imagepreview_path,
                    "Mask":mask_path
                })
        except RequiredValue as e:
            return self.bad_request({"Message": str(e)})
        except NoFace as e:
            return self.bad_request({"Message": str(e)})
        except Exception as e:
            return self.bad_request({"Message": "Error During Color Eyes Process"})
        return self.bad_request(eyescolor_serializerhandler.errors)

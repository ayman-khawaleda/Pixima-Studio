from rest_framework.views import APIView
from PiximaStudio.AbstractView import RESTView
from .serializer import EyesColorSerializer, EyesResizeSerializer
from .serializerHandler import EyesColorSerializerHandler, EyesResizeSerializerHandler
from PiximaTools.FaceTools import EyesTool
from PiximaTools.Exceptions import RequiredValue, NoFace


class EyesColorToolView(RESTView):
    def post(self, request, format=None):
        eyescolor_tool = EyesTool.EyesColorTool()
        eyescolor_serializer = EyesColorSerializer(data=request.data)
        eyescolor_serializerhandler = EyesColorSerializerHandler(eyescolor_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                eyescolor_tool.request2data(request=request)()
                image_path = eyescolor_tool.save_image()
                imagepreview_path = eyescolor_tool.get_preview()
                mask_path = eyescolor_tool.save_mask()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                        "Mask": mask_path,
                    }
                )
            if eyescolor_serializerhandler.handle():
                eyescolor_tool.serializer2data(
                    eyescolor_serializer
                ).read_image().apply()
                image_path = eyescolor_tool.save_image()
                imagepreview_path = eyescolor_tool.get_preview()
                mask_path = eyescolor_tool.save_mask()
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
            print(e)
            return self.bad_request({"Message": "Error During Color Eyes Process"})
        return self.bad_request(eyescolor_serializerhandler.errors)


class EyesResizeToolView(RESTView):
    def post(self, request, format=None):
        eyesresize_tool = EyesTool.EyesResizeTool()
        eyesresize_serializer = EyesResizeSerializer(data=request.data)
        eyesresize_serializerhandler = EyesResizeSerializerHandler(
            eyesresize_serializer
        )
        try:
            if eyesresize_serializerhandler.handle():
                eyesresize_tool.serializer2data(eyesresize_serializer)
                return self.ok_request({"Message": eyesresize_serializer.data})
        except RequiredValue as e:
            return self.bad_request({"Message": str(e)})
        except NoFace as e:
            return self.bad_request({"Message": str(e)})
        except Exception as e:
            print(e)
            return self.bad_request({"Message": "Error During Eyes Resize Process"})
        return self.bad_request(eyesresize_serializerhandler.errors)

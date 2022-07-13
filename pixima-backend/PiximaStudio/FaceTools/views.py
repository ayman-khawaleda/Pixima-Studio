from rest_framework.views import APIView
from PiximaStudio.AbstractView import RESTView
from .serializer import (
    EyesColorSerializer,
    EyesResizeSerializer,
    NoseResizeSerializer,
    SmoothFaceSeializer,
    WhiteTeethToolSerializer,
)
from .serializerHandler import (
    EyesColorSerializerHandler,
    EyesResizeSerializerHandler,
    NoseResizeSerializerHandler,
    SmoothFaceSerializerHandler,
    WhiteTeethToolSerializerHandler,
)
from PiximaTools.FaceTools import EyesTool, NoseTool, FaceTools
from PiximaTools.Exceptions import RequiredValue, NoFace
import traceback


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
            if "Image" in request.data.keys() and request.data["Image"] != "":
                eyesresize_tool.request2data(request=request)()
                image_path = eyesresize_tool.save_image()
                imagepreview_path = eyesresize_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if eyesresize_serializerhandler.handle():
                eyesresize_tool.serializer2data(eyesresize_serializer).read_image()()
                image_path = eyesresize_tool.save_image()
                imagepreview_path = eyesresize_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except RequiredValue as e:
            return self.bad_request({"Message": str(e)})
        except NoFace as e:
            return self.bad_request({"Message": str(e)})
        except Exception as e:
            return self.bad_request({"Message": "Error During Eyes Resize Process"})
        return self.bad_request(eyesresize_serializerhandler.errors)


class NoseResizeToolView(RESTView):
    def post(self, request, format=None):
        noseresize_tool = NoseTool.NoseResizeTool()
        noseresize_serializer = NoseResizeSerializer(data=request.data)
        noseresize_serializerhandler = NoseResizeSerializerHandler(
            noseresize_serializer
        )
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                noseresize_tool.request2data(request=request)()
                image_path = noseresize_tool.save_image()
                imagepreview_path = noseresize_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if noseresize_serializerhandler.handle():
                noseresize_tool.serializer2data(
                    noseresize_serializer
                ).read_image().apply()
                image_path = noseresize_tool.save_image()
                imagepreview_path = noseresize_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except RequiredValue as e:
            return self.bad_request({"Message": str(e)})
        except NoFace as e:
            return self.bad_request({"Message": str(e)})
        except Exception as e:
            return self.bad_request({"Message": "Error During Nose Resize Process"})
        return self.bad_request(noseresize_serializerhandler.errors)


class SmoothFaceToolView(RESTView):
    
    def post(self, request, format=None):
        smoothface_tool = FaceTools.SmoothFaceTool()
        smoothface_serializer = SmoothFaceSeializer(data=request.data)
        smoothface_serializerhandler = SmoothFaceSerializerHandler(
            smoothface_serializer
        )
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                smoothface_tool.request2data(request=request)()
                image_path = smoothface_tool.save_image()
                imagepreview_path = smoothface_tool.get_preview()
                mask_path = smoothface_tool.save_mask()

                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                        "Mask": mask_path,
                    }
                )
            if smoothface_serializerhandler.handle():
                smoothface_tool.serializer2data(
                    smoothface_serializer
                ).read_image().apply()
                image_path = smoothface_tool.save_image()
                imagepreview_path = smoothface_tool.get_preview()
                mask_path = smoothface_tool.save_mask()
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
            return self.bad_request({"Message": "Error During Face Smoothing Process"})
        return self.bad_request(smoothface_serializerhandler.errors)

class WhiteTeethToolView(RESTView):
    def post(self, request, format=None):
        whiteteeth_serializer = WhiteTeethToolSerializer(data=request.data)
        whiteteeth_serializerhandler = WhiteTeethToolSerializerHandler(
            whiteteeth_serializer
        )
        try:
            if whiteteeth_serializerhandler.handle():
                return self.ok_request(whiteteeth_serializer.data)
        except RequiredValue as e:
            return self.bad_request({"Message": str(e)})
        except NoFace as e:
            return self.bad_request({"Message": str(e)})
        except Exception as e:
            return self.bad_request({"Message": "Error During Whiteing Teeth Process"})
        return self.bad_request(whiteteeth_serializerhandler.errors)

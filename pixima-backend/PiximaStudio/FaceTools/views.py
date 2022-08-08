import traceback
from PiximaStudio.AbstractView import RESTView
from .serializer import (
    EyesColorSerializer,
    EyesResizeSerializer,
    NoseResizeSerializer,
    SmoothFaceSeializer,
    WhiteTeethToolSerializer,
    ColorLipsToolSerializer,
    SmileToolSerializer,
)
from .serializerHandler import (
    EyesColorSerializerHandler,
    EyesResizeSerializerHandler,
    NoseResizeSerializerHandler,
    SmoothFaceSerializerHandler,
    WhiteTeethToolSerializerHandler,
    ColorLipsToolSerializerHandler,
    SmileToolSerializerHandler,
)
from PiximaTools.FaceTools import EyesTool, NoseTool, FaceTools
from PiximaTools.Exceptions import RequiredValue, NoFace
from Core.models import ImageModel, ImageOperationsModel


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
                ImageObj = ImageModel.objects.get(id=eyescolor_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="EyesColorTool"
                ).save()
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
                ImageObj = ImageModel.objects.get(id=eyesresize_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="EyesResizeTool"
                ).save()
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
                ImageObj = ImageModel.objects.get(id=noseresize_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="NoseResizeTool"
                ).save()
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
                ImageObj = ImageModel.objects.get(id=smoothface_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="SmoothFaceTool"
                ).save()
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
        white_tool = FaceTools.WhiteTeethTool()
        whiteteeth_serializer = WhiteTeethToolSerializer(data=request.data)
        whiteteeth_serializerhandler = WhiteTeethToolSerializerHandler(
            whiteteeth_serializer
        )
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                white_tool.request2data(request=request)()
                image_path = white_tool.save_image()
                imagepreview_path = white_tool.get_preview()
                mask_path = white_tool.save_mask()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                        "Mask": mask_path,
                    }
                )
            if whiteteeth_serializerhandler.handle():
                white_tool.serializer2data(whiteteeth_serializer).read_image().apply()
                ImageObj = ImageModel.objects.get(id=whiteteeth_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="WhiteTeethTool"
                ).save()
                image_path = white_tool.save_image()
                imagepreview_path = white_tool.get_preview()
                mask_path = white_tool.save_mask()
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
            return self.bad_request({"Message": "Error During Whiteing Teeth Process"})
        return self.bad_request(whiteteeth_serializerhandler.errors)


class ColorLipsToolView(RESTView):
    def post(self, request, format=None):
        colorlips_tool = FaceTools.ColorLipsTool()
        colorlips_serializer = ColorLipsToolSerializer(data=request.data)
        colorlips_serializerhandler = ColorLipsToolSerializerHandler(
            colorlips_serializer
        )
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                colorlips_tool.request2data(request)()
                image_path = colorlips_tool.save_image()
                imagepreview_path = colorlips_tool.get_preview()
                mask_path = colorlips_tool.save_mask()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                        "Mask": mask_path,
                    }
                )
            if colorlips_serializerhandler.handle():
                colorlips_tool.serializer2data(colorlips_serializer).read_image()()
                ImageObj = ImageModel.objects.get(id=colorlips_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="ColorLipsTool"
                ).save()
                image_path = colorlips_tool.save_image()
                imagepreview_path = colorlips_tool.get_preview()
                mask_path = colorlips_tool.save_mask()
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
            return self.bad_request(
                {"Message": "Error During Change Color Lips Process"}
            )
        return self.bad_request(colorlips_serializerhandler.errors)


class SmileToolView(RESTView):
    def post(self, request, format=None):
        smile_tool = FaceTools.SmileTool()
        smile_serializer = SmileToolSerializer(data=request.data)
        smile_serializerhandler = SmileToolSerializerHandler(smile_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                smile_tool.request2data(request)()
                image_path = smile_tool.save_image()
                imagepreview_path = smile_tool.get_preview()
                mask_path = smile_tool.save_mask()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                        "Mask": mask_path,
                    }
                )
            if smile_serializerhandler.handle():
                smile_tool.serializer2data(smile_serializer).read_image()()
                ImageObj = ImageModel.objects.get(id=smile_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="SmileTool"
                ).save()
                image_path = smile_tool.save_image()
                imagepreview_path = smile_tool.get_preview()
                mask_path = smile_tool.save_mask()
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
            return self.bad_request(
                {"Message": "Error During Smile Adjustment Process"}
            )
        return self.bad_request(smile_serializerhandler.errors)

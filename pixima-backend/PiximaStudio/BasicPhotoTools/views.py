import traceback
from .serializer import (
    ChangeColorToolSerializer,
    ContrastImageSerializer,
    CropImageSerializer,
    FlipImageSerializer,
    ResizeImageSerializer,
    RotateImageSerializer,
    SaturationImageSerializer,
)
from .serializerHandler import (
    CropImageSerializerHandler,
    FlipImageSerializerHandler,
    ResizeImageSerializerHandler,
    RotateImageSerializerHandler,
    ContrastImageSerializerHandler,
    SaturationImageSerializerHandler,
    ChangeColorToolSerializerHandler,
)
from PiximaTools.BasicTools import (
    ContrastTool,
    CropTool,
    FlipTool,
    ResizeTool,
    RotatTool,
    SaturationTool,
    ChangeColorTool,
)
from Core.models import ImageModel, ImageOperationsModel
from PiximaStudio.AbstractView import RESTView
from PiximaTools.Exceptions import ClickedOutOfBound, NoFace, RequiredValue


class CropToolView(RESTView):
    def post(self, request, format=None):
        crop_tool = CropTool()
        crop_serializer = CropImageSerializer(data=request.data)
        im_handler = CropImageSerializerHandler(crop_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                crop_tool.request2data(request=request).apply()
                image_path = crop_tool.save_image()
                imagepreview_path = crop_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                crop_tool.serializer2data(
                    serializer=crop_serializer
                ).read_image().apply()
                ImageObj = ImageModel.objects.get(id=crop_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="CropTool"
                ).save()
                image_path = crop_tool.save_image()
                imagepreview_path = crop_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return self.bad_request({"Message": "Error During Crop Process"})
        return self.bad_request(im_handler.errors)


class FlipToolView(RESTView):
    def post(self, request, format=None):
        flip_tool = FlipTool()
        flip_serializer = FlipImageSerializer(data=request.data)
        im_handler = FlipImageSerializerHandler(flip_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                flip_tool.request2data(request=request).apply()
                image_path = flip_tool.save_image()
                imagepreview_path = flip_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                flip_tool.serializer2data(flip_serializer).read_image()()
                ImageObj = ImageModel.objects.get(id=flip_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="FlipTool"
                ).save()
                image_path = flip_tool.save_image()
                imagepreview_path = flip_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return self.bad_request({"Message": "Error During Flip Process"})
        return self.bad_request(im_handler.errors)


class RotateToolView(RESTView):
    def post(self, request, format=None):
        rotate_tool = RotatTool()
        rotate_serializer = RotateImageSerializer(data=request.data)
        im_handler = RotateImageSerializerHandler(rotate_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                rotate_tool.request2data(request=request).apply()
                image_path = rotate_tool.save_image()
                imagepreview_path = rotate_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                rotate_tool.serializer2data(rotate_serializer).read_image()()
                ImageObj = ImageModel.objects.get(id=rotate_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="RotateTool"
                ).save()
                image_path = rotate_tool.save_image()
                imagepreview_path = rotate_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return self.bad_request({"Message": "Error During Rotate Process"})
        return self.bad_request(im_handler.errors)


class ResizeToolView(RESTView):
    def post(self, request, format=None):
        resize_tool = ResizeTool()
        resize_serializer = ResizeImageSerializer(data=request.data)
        im_handler = ResizeImageSerializerHandler(resize_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                resize_tool.request2data(request=request).apply()
                image_path = resize_tool.save_image()
                imagepreview_path = resize_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                resize_tool.serializer2data(resize_serializer).read_image()()
                ImageObj = ImageModel.objects.get(id=resize_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="ResizeTool"
                ).save()
                image_path = resize_tool.save_image()
                imagepreview_path = resize_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return self.bad_request({"Message": "Error During Resize Process"})

        return self.bad_request(im_handler.errors)


class ContrastToolView(RESTView):
    def post(self, request, format=None):
        contrast_tool = ContrastTool()
        contrast_serializer = ContrastImageSerializer(data=request.data)
        im_handler = ContrastImageSerializerHandler(contrast_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                contrast_tool.request2data(request=request)()
                image_path = contrast_tool.save_image()
                imagepreview_path = contrast_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                contrast_tool.serializer2data(contrast_serializer).read_image().apply()
                ImageObj = ImageModel.objects.get(id=contrast_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="ContrastTool"
                ).save()
                image_path = contrast_tool.save_image()
                imagepreview_path = contrast_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return self.bad_request(
                {"Message": "Error During Contrast&Brightness Adjustment Process"}
            )

        return self.bad_request(im_handler.errors)


class SaturationToolView(RESTView):
    def post(self, request, format=None):
        saturation_tool = SaturationTool()
        saturation_serializer = SaturationImageSerializer(data=request.data)
        im_handler = SaturationImageSerializerHandler(saturation_serializer)
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                saturation_tool.request2data(request=request)()
                image_path = saturation_tool.save_image()
                imagepreview_path = saturation_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if im_handler.handle():
                saturation_tool.serializer2data(
                    saturation_serializer
                ).read_image().apply()
                ImageObj = ImageModel.objects.get(id=saturation_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="SaturationTool"
                ).save()
                image_path = saturation_tool.save_image()
                imagepreview_path = saturation_tool.get_preview()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return self.bad_request(
                {"Message": "Error During Saturation Adjustment Process"}
            )
        return self.bad_request(im_handler.errors)


class ChangeColorToolView(RESTView):
    def post(self, request, format=None):
        changecolor_tool = ChangeColorTool()
        changecolor_serializer = ChangeColorToolSerializer(data=request.data)
        im_handler = ChangeColorToolSerializerHandler(changecolor_serializer)

        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                changecolor_tool.request2data(request=request)()
                image_path = changecolor_tool.save_image()
                imagepreview_path = changecolor_tool.get_preview()
                mask_path = changecolor_tool.save_mask()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                        "Mask": mask_path,
                    }
                )
            if im_handler.handle():
                changecolor_tool.serializer2data(
                    changecolor_serializer
                ).read_image().apply()
                ImageObj = ImageModel.objects.get(id=changecolor_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="ChangeColorTool"
                ).save()
                image_path = changecolor_tool.save_image()
                imagepreview_path = changecolor_tool.get_preview()
                mask_path = changecolor_tool.save_mask()
                return self.ok_request(
                    {
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                        "Mask": mask_path,
                    }
                )

        except (ClickedOutOfBound, RequiredValue, NoFace) as e:
            return self.bad_request({"Message": str(e)})

        except Exception as e:
            return self.bad_request({"Message": "Error During Change Color Process"})

        return self.bad_request(im_handler.errors)

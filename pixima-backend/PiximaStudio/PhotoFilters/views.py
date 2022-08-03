import traceback
from . import serializer, serializerHandler
from PiximaTools import Filters
from Core.models import ImageModel,ImageOperationsModel
from PiximaStudio.AbstractView import RESTView


class GlitchFilterView(RESTView):
    def post(self, request, format=None):
        glitch_filter = Filters.GlitchFilter()
        glicth_serializer = serializer.GlitchFilterSerializer(data=request.data)
        filter_handler = serializerHandler.GlitchFilterSerializerHandler(
            glicth_serializer
        )
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                glitch_filter.request2data(request=request)()
                image_path = glitch_filter.save_image()
                imagepreview_path = glitch_filter.get_preview()
                return self.ok_request({
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if filter_handler.handle():
                image_path = (
                    glitch_filter.serializer2data(glicth_serializer)
                    .read_image()()
                    .save_image()
                )
                imagepreview_path = glitch_filter.get_preview()
                ImageObj = ImageModel.objects.get(id=glicth_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="GlitchFilter"
                ).save()

                return self.ok_request({
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return self.bad_request({"Message": "Error In Glitch Filter Request"})
        return self.bad_request(filter_handler.errors)


class CircleFilterView(RESTView):
    def post(self, request, format=None):
        circles_filter = Filters.CirclesFilter()
        circles_serializer = serializer.CirclesFilterSerializer(data=request.data)
        filter_handler = serializerHandler.CirclesFilterSerializerHandler(
            circles_serializer
        )
        try:
            if "Image" in request.data.keys() and request.data["Image"] != "":
                file = request.data["Image"].file
                circles_filter.request2data(request=request)()
                image_path = circles_filter.save_image()
                imagepreview_path = circles_filter.get_preview()
                return self.ok_request({
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
            if filter_handler.handle():
                circles_filter.serializer2data(
                    serializer=circles_serializer
                ).read_image().apply()
                image_path = circles_filter.save_image()
                imagepreview_path = circles_filter.get_preview()
                ImageObj = ImageModel.objects.get(id=circles_serializer["id"].value)
                ImageOperationsModel.objects.create(
                    image=ImageObj, operation_name="CircleFilter"
                ).save()
                return self.ok_request({
                        "Image": image_path,
                        "ImagePreview": imagepreview_path,
                    }
                )
        except Exception as e:
            return self.bad_request({"Message": "Error In Circles Filter Request"})
        return self.bad_request(filter_handler.errors)

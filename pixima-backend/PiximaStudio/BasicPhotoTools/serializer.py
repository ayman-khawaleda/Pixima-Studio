from rest_framework.serializers import Serializer,UUIDField,ImageField,CharField,IntegerField,BooleanField


class ImageHandlerSerializer(Serializer):
    id = UUIDField(default='',required=False,allow_null=True,format='hex_verbose')
    Image = ImageField(default='',required=False,allow_null=True)
    Preview = CharField(default='None',required=False)


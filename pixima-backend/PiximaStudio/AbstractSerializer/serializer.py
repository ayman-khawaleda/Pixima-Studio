from rest_framework.serializers import (
    Serializer,
    UUIDField,
    ImageField,
    CharField,
    IntegerField,
)

class ImageSerializer(Serializer):

    id = UUIDField(required=False, allow_null=True, format="hex_verbose")
    ImageIndex = IntegerField(default=0, required=False, allow_null=True)
    Image = ImageField(default="", required=False, allow_null=True)
    Preview = CharField(default="None", required=False)


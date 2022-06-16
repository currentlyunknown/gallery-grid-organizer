import uuid
from typing import Union

from django.db.models.query import EmptyQuerySet

from gallery.models import Image


class ImageService:
    def __init__(self):
        pass

    @classmethod
    def get_all_images(cls) -> Union[Image, EmptyQuerySet]:
        return Image.objects.order_by("-weight")

    @classmethod
    def get_image_by_id(cls, uuid: uuid) -> Union[Image, None]:
        try:
            result = Image.objects.get(id=uuid)
        except Image.DoesNotExist:
            result = None
        return result

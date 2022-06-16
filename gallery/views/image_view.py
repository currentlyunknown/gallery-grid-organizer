import logging

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from gallery.serializers import ImageSerializer
from gallery.services.image_service import ImageService

logger = logging.getLogger("project")


class ImageGetView(GenericAPIView):
    """View to get one image"""

    def get(self, request, uuid) -> Response:
        logger.info(f"/image/get: {request.user} {uuid}")
        image = ImageService.get_image_by_id(uuid)
        if not image:
            logger.error(f"/image/get: {request.user} {uuid} Not found")
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = ImageSerializer(image, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageGetListView(ListAPIView):
    """
    Image list view
    """

    serializer_class = ImageSerializer
    ordering = "grid_position"

    def get_queryset(self):
        logger.info(f"/image/list: {self.request.user}")
        return ImageService.get_all_images()

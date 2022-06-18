import logging

from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from gallery.models import Image
from gallery.serializers import EventCreateSerializer
from gallery.services.events_service import EventService

logger = logging.getLogger("project")


class EventPostView(GenericAPIView):
    """
    View to post events:
    This endpoint is called every time an image receives some event on it (view, or click).
    These events will be the ones used to optimize the gallery grid later.
    """

    def post(self, request, *args, **kwargs) -> Response:
        logger.info(f"/event/post: {request.user} posting {request.data} event.")
        image = get_object_or_404(Image, id=kwargs.get("uuid"))
        serializer = EventCreateSerializer(data=request.data)
        if not serializer.is_valid() or not request.data.get("eventType"):
            logger.error(
                f"/event/post: Error when {request.user} tried to post event with {request.data}."
            )
            return Response(
                {"There request payload is not well formed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        event = EventService.create_event(
            image=image, event_type=request.data.get("eventType")
        )
        return Response(
            EventCreateSerializer(event, many=False).data,
            status=status.HTTP_201_CREATED,
        )

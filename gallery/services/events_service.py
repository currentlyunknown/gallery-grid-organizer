from gallery.models import Event, Image


class EventService:
    @classmethod
    def create_event(cls, image: Image, event_type: str) -> Event:
        """Given an event type and an Image created the event object and returns it."""
        if event_type == "click":
            event = Event.objects.create(image=image, clicks=1)
        else:
            event = Event.objects.create(image=image, views=1)
        return event

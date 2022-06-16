from django.db.models import Sum
from rest_framework import serializers

from gallery.models import Event, Image


class EventCreateSerializer(serializers.ModelSerializer):
    """This serializer is only for Event creation."""

    class Meta:
        model = Event
        fields = ["clicks", "views", "created"]
        read_only_fields = ("created",)


class EventSerializer(serializers.ModelSerializer):
    """This serializer is for representation inside Image Summing clicks and views."""

    clicks = serializers.SerializerMethodField("get_clicks_info")
    views = serializers.SerializerMethodField("get_views_info")

    def get_clicks_info(self, obj) -> int:
        events = obj.all()
        if events:
            clicks = events.aggregate(clicks_sum=Sum("clicks"))
            return clicks.get("clicks_sum")
        return 0

    def get_views_info(self, obj) -> int:
        events = obj.all()
        if events:
            clicks = events.aggregate(views_sum=Sum("views"))
            return clicks.get("views_sum")
        return 0

    class Meta:
        model = Event
        fields = ["clicks", "views", "created"]
        read_only_fields = ("created",)


class ImageSerializer(serializers.ModelSerializer):
    events = EventSerializer()
    weight = serializers.DecimalField(
        max_digits=5, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = Image
        ordering = "-weight"
        fields = ["id", "name", "weight", "grid_position", "url", "events"]

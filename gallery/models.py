import uuid

from django.db import models
from django.db.models import Sum
from django_extensions.db.models import TimeStampedModel

from .constants import CLICKS_RATIO, VIEWS_RATIO


class Image(models.Model):
    """Represents an image which will be part of the Gallery."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=15, blank=True)
    weight = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        default=0.0,
        help_text="Calculated ROI with data from events.",
    )
    grid_position = models.IntegerField(
        default=0, help_text="Its order on the output grid."
    )
    url = models.URLField(help_text="URI where the image is located at.")

    def __str__(self) -> str:
        return f"{self.id} - {self.name} - {self.weight} - {self.grid_position}"

    class Meta:
        ordering = ["-weight"]


class Event(TimeStampedModel):
    """
    When an image is viewed or clicked this event is created.
    Consult 'created' field to get the timestamped datetime.
    """

    views = models.IntegerField(default=0, help_text="Time the image has been seen.")
    clicks = models.IntegerField(
        default=0, help_text="Time the image has been clicked."
    )
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="events")

    def __str__(self) -> str:
        return f"{self.created} - {self.views} - {self.clicks}"

    def save(self, **kwargs) -> object:
        """
        This approach is to avoid signals. They don't work when bulk_update or bulk_create
        """
        super().save(**kwargs)
        # select_for_update of atomic.transaction() would also work
        image = Image.objects.select_for_update().get(id=self.image.id)
        total_views = image.events.aggregate(sum_views=Sum("views")).get("sum_views")
        total_clicks = image.events.aggregate(sum_clicks=Sum("clicks")).get(
            "sum_clicks"
        )
        image.weight = total_views * VIEWS_RATIO + total_clicks * CLICKS_RATIO
        image.save()

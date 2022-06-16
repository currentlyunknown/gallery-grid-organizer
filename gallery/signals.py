import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from gallery.models import Image
from gallery.utils import order_dataset

logger = logging.getLogger("project")


@receiver(post_save, sender=Image)
def reorder_grid(sender, instance, **kwargs):
    """Signal to change the Order of images if weight has changed"""
    current = instance
    previous = Image.objects.get(id=instance.id)
    # if weight has changed, or current is a new object all is reordered
    if previous.weight != current.weight or current.grid_position == 0:
        order_dataset()

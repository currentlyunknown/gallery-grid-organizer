import logging

from celery import Celery

from gallery.models import Image

celery = Celery()
logger = logging.getLogger("project")


@celery.task()
def order_dataset():
    """
    Async task to reorder grid_position.
    Dataset is a Queryset of Images already ordered by Weight. See model, meta option.
    The more weight the higher the grid_position will be
    """

    dataset = Image.objects.all()
    for index, elem in enumerate(dataset, start=1):
        elem.grid_position = index
        elem.save()

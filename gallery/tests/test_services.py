import pytest

from gallery.models import Image
from gallery.services.events_service import EventService
from gallery.services.image_service import ImageService


@pytest.mark.django_db
def test_service_one_image():
    # given
    image = Image.objects.create(weight=100, grid_position=1)

    # when
    service_result = ImageService.get_image_by_id(image.id)

    # then
    assert service_result is not None
    assert service_result.weight == image.weight


@pytest.mark.django_db
def test_service_many_images():
    # given
    Image.objects.create(weight=100, grid_position=1)
    Image.objects.create(weight=10, grid_position=2)
    Image.objects.create(weight=1, grid_position=3)

    # when
    service_result = ImageService.get_all_images()

    # then
    assert service_result is not None
    assert service_result.count() == Image.objects.count()
    assert [i.weight for i in service_result] == [100.00, 10.00, 1.00]


@pytest.mark.django_db
def test_service_no_image():
    # when
    service_result = ImageService.get_image_by_id(None)

    # then
    assert service_result is None


@pytest.mark.django_db
def test_service_events():
    # given
    image = Image.objects.create(weight=100, grid_position=1)

    # when
    event_click = EventService.create_event(image=image, event_type="click")
    event_view = EventService.create_event(image=image, event_type="view")

    # then
    assert event_view is not None
    assert event_click is not None
    assert event_view.views == 1
    assert event_click.clicks == 1

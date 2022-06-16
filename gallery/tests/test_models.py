import pytest

from gallery.models import Event, Image


@pytest.mark.django_db
def test_image():
    # given
    image = Image.objects.create(weight=100, grid_position=1)

    # when
    output = f"{image.id} - {image.name} - {image.weight} - {image.grid_position}"

    # then
    assert image is not None
    assert str(image) == output


@pytest.mark.django_db
def test_event():
    # given
    image = Image.objects.create(weight=100, grid_position=1)
    event = Event.objects.create(image=image, views=2, clicks=4)

    # when
    output = f"{event.created} - {event.views} - {event.clicks}"

    # then
    assert event is not None
    assert str(event) == output

import pytest

from gallery.models import Event, Image
from gallery.serializers import EventSerializer, ImageSerializer


@pytest.mark.django_db
def test_serializer_one_image():
    # given
    image = Image.objects.create(weight=100, grid_position=1)

    # when
    serializer = ImageSerializer(image)

    # then
    assert serializer.data is not None
    assert serializer.data.get("weight") == image.weight


@pytest.mark.django_db
def test_serializer_many_images():
    # given
    Image.objects.create(weight=100, grid_position=1)
    Image.objects.create(weight=10, grid_position=2)
    Image.objects.create(weight=1, grid_position=3)

    # when
    serializer = ImageSerializer(Image.objects.all(), many=True)

    # then
    assert serializer.data is not None
    assert len(serializer.data) == Image.objects.count()
    assert [i.get("weight") for i in serializer.data] == [100.00, 10.00, 1.00]


@pytest.mark.django_db
def test_serializer_events():
    # given
    image = Image.objects.create(weight=100, grid_position=1)
    Event.objects.create(clicks=110, image=Image.objects.first())
    Event.objects.create(clicks=220, image=Image.objects.first())
    Event.objects.create(views=200, image=Image.objects.first())

    # when
    image_serializer = ImageSerializer(image)
    event_serializer = EventSerializer(Event.objects.all(), many=False)

    # then
    assert image_serializer.data is not None
    assert event_serializer.data is not None
    assert image_serializer.data.get("events") == event_serializer.data
    assert event_serializer.data == {"clicks": 330, "views": 200}

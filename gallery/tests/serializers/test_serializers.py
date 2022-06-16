from django.test import TestCase

from gallery.models import Event, Image
from gallery.serializers import EventSerializer, ImageSerializer


class ImageSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.image = Image.objects.create(weight=100, grid_position=1)

    def test_serializer_get_one_image(self):
        serializer = ImageSerializer(self.image)
        self.assertIsNotNone(serializer.data)
        self.assertAlmostEqual(serializer.data.get("weight"), self.image.weight)

    def test_serializer_list_images(self):
        Image.objects.create(weight=100, grid_position=1)
        Image.objects.create(weight=10, grid_position=2)
        Image.objects.create(weight=1, grid_position=3)
        serializer = ImageSerializer(Image.objects.all(), many=True)
        self.assertIsNotNone(serializer.data)
        self.assertEqual(len(serializer.data), Image.objects.count())

    def test_serializer_not_found(self):
        with self.assertRaises(Image.DoesNotExist):
            serializer = ImageSerializer(Image.objects.get(name="invented"))
            self.assertIsNone(serializer.data)

    def test_serializer_list_ordering_ok(self):
        Image.objects.create(weight=1)
        Image.objects.create(weight=10)
        Image.objects.create(weight=20)
        serializer = ImageSerializer(Image.objects.all(), many=True)
        self.assertIsNotNone(serializer.data)
        self.assertEqual(
            [i.get("weight") for i in serializer.data], [100.00, 20.00, 10.00, 1.00]
        )


class EventSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.image = Image.objects.create(weight=100, grid_position=1)
        self.event_a = Event.objects.create(clicks=110, image=Image.objects.first())
        self.event_b = Event.objects.create(clicks=220, image=Image.objects.first())
        self.event_views = Event.objects.create(views=200, image=Image.objects.first())

    def test_event_serializer_inside_image(self):
        serializer = ImageSerializer(self.image)
        self.assertEqual(
            serializer.data.get("events"),
            EventSerializer(Event.objects.all(), many=False).data,
        )

    def test_list_events_serializer(self):
        serializer = EventSerializer(Event.objects.all(), many=False)
        self.assertIsNotNone(serializer.data)
        self.assertEqual(serializer.data, {"clicks": 330, "views": 200})

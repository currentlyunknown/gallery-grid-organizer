from django.test import TestCase

from gallery.models import Image, Event


class ImageTestCase(TestCase):

    def setUp(self):
        self.image = Image.objects.create(weight=100, grid_position=1)

    def test_image_creation(self):
        result = Image.objects.create(weight=100, grid_position=1)
        self.assertIsNotNone(result)

    def test_representation(self):
        output = f"{self.image.id} - {self.image.name} - {self.image.weight} - {self.image.grid_position}"
        self.assertEqual(output, self.image.__str__())


class EventTestCase(TestCase):

    def setUp(self):
        self.image = Image.objects.create(weight=100, grid_position=1)

    def test_image_creation(self):
        result = Event.objects.create(image=self.image)
        self.assertIsNotNone(result)

    def test_representation(self):
        result = Event.objects.create(image=self.image, views=2, clicks=4)
        output = f"{result.created} - {result.views} - {result.clicks}"
        self.assertEqual(output, result.__str__())

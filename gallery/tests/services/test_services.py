from django.test import TestCase

from gallery.models import Image
from gallery.services.events_service import EventService
from gallery.services.image_service import ImageService


class ImageServiceTestCase(TestCase):
    def setUp(self):
        self.image = Image.objects.create(weight=100, grid_position=1)

    def test_service_get_one_image(self):
        service_result = ImageService.get_image_by_id(self.image.id)
        self.assertIsNotNone(service_result)
        self.assertEqual(service_result.weight, self.image.weight)

    def test_service_list_images(self):
        Image.objects.create(weight=100, grid_position=1)
        Image.objects.create(weight=10, grid_position=2)
        Image.objects.create(weight=1, grid_position=3)
        service_result = ImageService.get_all_images()
        self.assertIsNotNone(service_result)
        self.assertEqual(service_result.count(), Image.objects.count())

    def test_service_image_not_found(self):
        service_result = ImageService.get_image_by_id(None)
        self.assertIsNone(service_result)

    def test_service_list_ordering_ok(self):
        Image.objects.create(weight=1)
        Image.objects.create(weight=10)
        Image.objects.create(weight=20)
        service_result = ImageService.get_all_images()
        self.assertIsNotNone(service_result)
        self.assertEqual([i.weight for i in service_result], [100, 20, 10, 1])


class EventsServiceTestCase(TestCase):
    def test_event_click_service_creation(self):
        image = Image.objects.create(weight=100, grid_position=1)
        event = EventService.create_event(image=image, event_type="click")
        self.assertIsNotNone(event)
        self.assertEqual(event.clicks, 1)

    def test_event_view_service_creation(self):
        image = Image.objects.create(weight=100, grid_position=1)
        event = EventService.create_event(image=image, event_type="view")
        self.assertIsNotNone(event)
        self.assertEqual(event.views, 1)

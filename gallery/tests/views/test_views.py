import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from gallery.models import Event, Image


class ImageViewsTestCase(TestCase):
    """Tests for Images views"""

    def setUp(self) -> None:
        self.image = Image.objects.create(weight=100, grid_position=1)
        self.client = APIClient()

    def test_view_get_one_image(self):
        url = reverse("gallery:image-get", args=[self.image.id])
        response = self.client.get(url)
        self.assertEqual(response.data.get("id"), str(self.image.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_list_images(self):
        [Image.objects.create(weight=i) for i in range(4)]
        url = reverse("gallery:images-list")
        response = self.client.get(url)
        self.assertEqual(
            [i.get("id") for i in response.data.get("results")],
            [str(i.id) for i in Image.objects.all()],
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_image_not_found(self):
        random_uuid = uuid.UUID("{12345678-1234-5678-1234-567812345678}")
        url = reverse("gallery:image-get", args=[str(random_uuid)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EventViewTestCase(TestCase):
    def setUp(self) -> None:
        self.image = Image.objects.create(weight=100, grid_position=1)
        self.client = APIClient()

    def test_post_events(self):
        url = reverse("gallery:event-post", args=[self.image.id])
        response = self.client.post(url, {"eventType": "click"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.image.events.first(), Event.objects.first())

    def test_post_image_not_found(self):
        random_uuid = uuid.UUID("{12345678-1234-5678-1234-567812345678}")
        url = reverse("gallery:event-post", args=[str(random_uuid)])
        response = self.client.post(url, {"eventType": "click"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_bad_formed_body(self):
        url = reverse("gallery:event-post", args=[self.image.id])
        response = self.client.post(url, {"a": 11})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

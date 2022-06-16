import uuid

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from gallery.models import Event, Image


@pytest.mark.django_db
class TestImageViews:
    def test_view_one_image(self):
        image = Image.objects.create(weight=100, grid_position=1)
        client = APIClient()
        url = reverse("gallery:image-get", args=[image.id])
        response = client.get(url)
        assert response.data.get("id") == str(image.id)
        assert response.status_code == status.HTTP_200_OK

    def test_view_list_images(self):
        [Image.objects.create(weight=i) for i in range(4)]
        client = APIClient()
        url = reverse("gallery:images-list")
        response = client.get(url)
        assert [i.get("id") for i in response.data.get("results")] == [
            str(i.id) for i in Image.objects.all()
        ]
        assert response.status_code == status.HTTP_200_OK

    def test_view_image_not_found(self):
        client = APIClient()
        random_uuid = uuid.UUID("{12345678-1234-5678-1234-567812345678}")
        url = reverse("gallery:image-get", args=[str(random_uuid)])
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestEventViews:
    def test_post_event(self):
        image = Image.objects.create(weight=100, grid_position=1)
        client = APIClient()
        url = reverse("gallery:event-post", args=[image.id])
        response = client.post(url, {"eventType": "click"})
        assert response.status_code == status.HTTP_201_CREATED
        assert image.events.first() == Event.objects.first()

    def test_view_list_images(self):
        [Image.objects.create(weight=i) for i in range(4)]
        client = APIClient()
        url = reverse("gallery:images-list")
        response = client.get(url)
        assert [i.get("id") for i in response.data.get("results")] == [
            str(i.id) for i in Image.objects.all()
        ]
        assert response.status_code == status.HTTP_200_OK

    def test_post_event_image_not_found(self):
        client = APIClient()
        random_uuid = uuid.UUID("{12345678-1234-5678-1234-567812345678}")
        url = reverse("gallery:event-post", args=[str(random_uuid)])
        response = client.post(url, {"eventType": "click"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_event_bad_formed_body(self):
        image = Image.objects.create(weight=100, grid_position=1)
        client = APIClient()
        url = reverse("gallery:event-post", args=[image.id])
        response = client.post(url, {"a": 11})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

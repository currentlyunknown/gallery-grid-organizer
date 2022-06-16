from django.test import TestCase
from rest_framework.test import APIClient

from gallery.models import Image

IMAGES_LOT_NUMBER = 10


class EndToEndTestCase(TestCase):
    """Tests to cover full flows"""

    def setUp(self) -> None:

        [Image.objects.create(weight=i) for i in range(IMAGES_LOT_NUMBER)]
        self.client = APIClient()

    def test_view_get_one_image(self):
        """Just checking the right order works"""
        self.assertEqual(
            [i.grid_position for i in Image.objects.all()],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        )


#  Yup, lots of e2e tests are missing. However, I cant dedicate more time

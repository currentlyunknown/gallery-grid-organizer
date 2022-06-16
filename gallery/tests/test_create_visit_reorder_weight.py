import pytest

from gallery.models import Image

IMAGES_LOT_NUMBER = 10


@pytest.mark.django_db
class TestEndToEnd:
    """Tests to cover full flows"""

    def test_order(self):
        """Just checking the right order"""
        [Image.objects.create(weight=i) for i in range(IMAGES_LOT_NUMBER)]
        assert [i.grid_position for i in Image.objects.all()] == [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
        ]

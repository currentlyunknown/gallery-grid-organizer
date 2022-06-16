from django.urls import path

from gallery.views.events_view import EventPostView
from gallery.views.image_view import ImageGetListView, ImageGetView

app_name = "gallery"

urlpatterns = [
    path("images/<uuid:uuid>/events", EventPostView.as_view(), name="event-post"),
    path("images/<uuid:uuid>", ImageGetView.as_view(), name="image-get"),
    path("images/", ImageGetListView.as_view(), name="images-list"),
]

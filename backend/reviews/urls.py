from django.urls import path
from .views import (
    TripTypeView,
    ImageStorageView,
    ReviewGetView,
    ReviewCreateView,
    ImageCreateView,
    ImageDeleteView,
    ReviewUpdateView,
    ReviewDeleteView,
)

urlpatterns = [
    path('get-trip-type/<str:id>', TripTypeView.as_view(), name='get-trip-type'),
    path('get-all-trip-type/', TripTypeView.as_view(), name='get-all-trip-type'),
    path('get-all-images/', ImageStorageView.as_view(), name='get-all-image'),
    path('get-image/<str:image_id>', ImageStorageView.as_view(), name='get-image'),
    path('get-images/<str:review_id>', ImageStorageView.as_view(), name='get-images-by-review'),
    path('get-all-reviews/', ReviewGetView.as_view(), name='get-all-review'),
    path('get-review/<str:review_id>', ReviewGetView.as_view(), name='get-review'),
    path('get-reviews-by-location/<str:location_id>', ReviewGetView.as_view(), name='get-review-by-location'),
    path('get-reviews-by-user/<str:user_id>', ReviewGetView.as_view(), name='get-review-by-user'),
    path('create-review/', ReviewCreateView.as_view(), name='create-review'),
    path('create-image/', ImageCreateView.as_view(), name='create-images'),
    path('delete-image/<str:image_id>', ImageDeleteView.as_view(), name='delete-image'),
    path('update-review/', ReviewUpdateView.as_view(), name='update-review'),
    path('delete-review/<str:id>', ReviewDeleteView.as_view(), name='delete-review'),
]

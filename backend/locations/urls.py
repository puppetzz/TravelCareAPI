from django.urls import path
from .views import (
    CategoryListView,
    LocationListByCategoryView,
    LocationCreateView,
    LocationListByCountryView,
    LocationListByProvinceView,
    LocationListByDistrictView,
    LocationView,
    LocationGetImageView,
)

urlpatterns = [
    path('get-all-category/', CategoryListView.as_view(), name='get-all-category'),
    path('get-all-location/<str:category_id>', LocationListByCategoryView.as_view(), name='get-all-location-with-category'),
    path('get-location/<str:location_id>', LocationView.as_view(), name='get-location'),
    path('get-location-with-country/<str:country_id>', LocationListByCountryView.as_view(), name='get-location-with-country'),
    path('get-location-with-country/<str:country_id>/<str:category_id>', LocationListByCountryView.as_view(), name='get-location-with-country-category'),
    path('get-location-with-province/<str:country_id>/<str:province_id>', LocationListByProvinceView.as_view(), name='get-location-with-province'),
    path('get-location-with-province/<str:country_id>/<str:province_id>/<str:category_id>', LocationListByProvinceView.as_view(), name='get-location-with-province-category'),
    path('get-location-with-district/<str:country_id>/<str:province_id>/<str:district_id>', LocationListByDistrictView.as_view(), name='get-location-with-district-category'),
    path('get-location-with-district/<str:country_id>/<str:province_id>/<str:district_id>/<str:category_id>', LocationListByDistrictView.as_view(), name='get-location-with-district-category'),
    path('get-all-location/', LocationListByCategoryView.as_view(), name='get-all-location'),
    path('create-location/', LocationCreateView.as_view(), name='create-location'),
    path('get-images/<str:location_id>', LocationGetImageView.as_view(), name='get-images'),
]

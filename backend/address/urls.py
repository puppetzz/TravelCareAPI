from django.urls import path, include
from .views import (
    CountryListView,
    ProvinceListView,
    DistrictListView,
    AddressListView
)

urlpatterns = [
    path('get-all-country/', CountryListView.as_view(), name='get-all-country'),
    path('get-country/<str:id>', CountryListView.as_view(), name='get-country'),
    path('get-list-province/<str:country_id>',
         ProvinceListView.as_view(), name='get-list-province'),
    path('get-list-district/<str:province_id>',
         DistrictListView.as_view(), name='get-list-district'),
    path('get-list-address/<str:country_id>',
         AddressListView.as_view(), name='get-list-address-country'),
    path('get-list-address/<str:country_id>/<str:province_id>',
         AddressListView.as_view(), name='get-list-address-province'),
    path('get-list-address/<str:country_id>/<str:province_id>/<str:district_id>/',
         AddressListView.as_view(), name='get-list-address-district'),
]

from django.urls import path, include
from .views import (
    CountryListView,
    ProvinceListView,
    DistrictListView,
    AddressListView,
    AddressCerateView,
    AddressDestroyView,
)

urlpatterns = [
    path('get-all-country/', CountryListView.as_view(), name='get-all-country'),
    path('get-country/<str:id>', CountryListView.as_view(), name='get-country'),
    path('get-list-province/<str:country_id>',
         ProvinceListView.as_view(), name='get-list-province'),
    path('get-province/<str:province_id>',
         ProvinceListView.as_view(), name='get-province'),
    path('get-list-district/<str:province_id>',
         DistrictListView.as_view(), name='get-list-district'),
    path('get-district/<str:district_id>',
         DistrictListView.as_view(), name='get-district'),
    path('get-list-address/<str:country_id>',
         AddressListView.as_view(), name='get-list-address-country'),
    path('get-list-address/<str:country_id>/<str:province_id>',
         AddressListView.as_view(), name='get-list-address-province'),
    path('get-list-address/<str:country_id>/<str:province_id>/<str:district_id>/',
         AddressListView.as_view(), name='get-list-address-district'),
    path('create-address/', AddressCerateView.as_view(), name='create-address'),
    path('delete-address/<str:id>',
         AddressDestroyView.as_view(), name='delete-address'),
]

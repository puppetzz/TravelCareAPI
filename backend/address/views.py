from rest_framework.views import APIView
from authentication.permissions import IsOwner
from .models import (
    Country,
    Province,
    District,
    Address
)
from .serializers import (
    CountrySerializer,
    ProvinceSerializer,
    DistrictSerializer,
    AddressGetSerializer,
    AddressCreateSerializer,
    AddressDestroySerializer,

)
from rest_framework.response import Response
from rest_framework import generics, status, permissions, mixins
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CountryListView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class ProvinceListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProvinceSerializer

    def get(self, request, *args, **kwargs):
        country_id = kwargs.get('country_id')
        if not country_id:
            return Response(
                {
                    'error': 'Country should not null'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        province = None
        if Country.objects.filter(id=country_id).exists():
            province = Province.objects.filter(
                country=Country.objects.get(id=country_id))
        if not province:
            return Response(
                {
                    'error': 'Country do have not province',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(province, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DistrictListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = DistrictSerializer

    def get(self, request, *args, **kwargs):
        province_id = kwargs.get('province_id')
        if not province_id:
            return Response(
                {
                    'error': 'province should not null'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        district = None
        if Province.objects.filter(id=province_id).exists():
            district = District.objects.filter(
                province=Province.objects.get(id=province_id))
        if not district:
            return Response(
                {
                    'error': 'Province do have not district',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(district, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressGetSerializer

    def get(self, request, *args, **kwargs):
        country_id = kwargs.get('country_id')
        province_id = kwargs.get('province_id')
        district_id = kwargs.get('district_id')

        if not country_id:
            return Response(
                {
                    'error': 'Country should not null.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not province_id:
            if not district_id:
                address = Address.objects.filter(
                    country=get_object_or_404(Country, id=country_id))
                serializer = AddressGetSerializer(address, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                {
                    'error': 'Province should not null.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not district_id:
            address = Address.objects.filter(
                country=get_object_or_404(Country, id=country_id)).filter(
                    province=get_object_or_404(Province, id=province_id)
            )

            serializer = AddressGetSerializer(address, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        address = Address.objects.filter(
            country=get_object_or_404(Country, id=country_id)).filter(
                province=get_object_or_404(Province, id=province_id)
        )

        serializer = self.serializer_class(address, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressCerateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AddressCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressDestroyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Address.objects.all()

    def delete(self, request, *args, **kwargs):
        address = get_object_or_404(self.queryset, id=kwargs.get('id'))
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

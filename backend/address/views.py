from rest_framework.views import APIView
from authentication.permissions import IsOwner
from .models import (
    Country,
    Province,
    District
)
from .serializers import (
    CountrySerializer,
    ProvinceSerializer,
    DistrictSerializer
)
from rest_framework.response import Response
from rest_framework import generics, status, permissions, mixins


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
    # permission_classes = [permissions.IsAuthenticated, ]
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

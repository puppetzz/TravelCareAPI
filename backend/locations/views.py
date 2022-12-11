from django.shortcuts import render
from .serializers import (
    CategorySerializer,
    LocationSerializer,
    LocationCreateSerializer,
)
from .models import Category, Location
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from address.models import Country, Province, District

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
class LocationListByCategoryView(generics.GenericAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        if category_id is None:
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        category  = get_object_or_404(Category, id=category_id)
        location = self.get_queryset().filter(category=category)
        serializer = self.serializer_class(location, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationListByCountryView(generics.GenericAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def get(self, request, *args, **kwargs):
        country_id = kwargs.get('country_id')
        category_id = kwargs.get('category_id')
        
        if not Country.objects.filter(id=country_id).exists():
            return Response(
                {
                    'error': 'Country does not exist.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        location = self.get_queryset().filter(address__country__id=country_id)
        if not category_id:
            serializer = self.serializer_class(location, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        category = get_object_or_404(Category, id=category_id)
        location = location.filter(category=category)
        serializer = self.serializer_class(location, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LocationListByProvinceView(generics.GenericAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def get(self, request, *args, **kwargs):
        country_id = kwargs.get('country_id')
        province_id = kwargs.get('province_id')
        category_id = kwargs.get('category_id')

        if not Country.objects.filter(id=country_id).exists():
            return Response(
                {
                    'error': 'Country does not exist.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not Province.objects.filter(id=province_id).exists():
            return Response(
                {
                    'error': 'Province does not exist.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        location = self.get_queryset().filter(
            address__country__id=country_id,
            address__province__id=province_id
            )
        if not category_id:
            serializer = self.serializer_class(location, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        category = get_object_or_404(Category, id=category_id)
        location = location.filter(category=category)
        serializer = self.serializer_class(location, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LocationListByDistrictView(generics.GenericAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def get(self, request, *args, **kwargs):
        country_id = kwargs.get('country_id')
        province_id = kwargs.get('province_id')
        district_id = kwargs.get('district_id')
        category_id = kwargs.get('category_id')

        if not Country.objects.filter(id=country_id).exists():
            return Response(
                {
                    'error': 'Country does not exist.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not Province.objects.filter(id=province_id).exists():
            return Response(
                {
                    'error': 'Province does not exist.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
            
        if not District.objects.filter(id=district_id).exists():
            return Response(
                {
                    'error': 'District does not exist.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        location = self.get_queryset().filter(
            address__country__id=country_id,
            address__province__id=province_id,
            address__district__id=district_id
            )
        if not category_id:
            serializer = self.serializer_class(location, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        category = get_object_or_404(Category, id=category_id)
        location = location.filter(category=category)
        serializer = self.serializer_class(location, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class LocationCreateView(generics.GenericAPIView):
    serializer_class = LocationCreateSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': 'Create location successfully.',
            },
            status=status.HTTP_200_OK
        )
from rest_framework import serializers
from .models import Category, Location
from address.serializers import (
    AddressGetSerializer, 
    AddressCreateSerializer
)
import uuid
from django.shortcuts import get_object_or_404

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
    
class LocationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    address = AddressGetSerializer()

    class Meta:
        model = Location
        fields = [
            'id',
            'address',
            'name',
            'rating',
            'category',
            'price_level',
            'description',
        ]

class LocationCreateSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=10)
    province = serializers.CharField(max_length=10)
    district = serializers.CharField(max_length=10)
    street_address = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    category = serializers.CharField(max_length=10)
    price_level = serializers.IntegerField(required=False)
    description = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        fields = [
            'country',
            'province',
            'district',
            'street_address',
            'name',
            'rating',
            'category',
            'price_level',
            'description',
        ]

    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        id = str(uuid.uuid4().int)[:9]
        
        address_data = dict()
        address_data['country'] = validated_data.get('country')
        address_data['province'] = validated_data.get('province')
        address_data['district'] = validated_data.get('district')
        address_data['street_address'] = validated_data.get('street_address')
        address_serializer = AddressCreateSerializer(data=address_data)
        address_serializer.is_valid()
        address = address_serializer.save()
        
        
        name = validated_data.get('name')
        rating = validated_data.get('rating')
        category_id = validated_data.get('category')
        category = get_object_or_404(Category, id=category_id)
        
        price_level = None
        if validated_data.get('price_level'):
            price_level = validated_data.get('price_level')
        
        description = None 
        if validated_data.get('description'):
            description = validated_data.get('description')
        
        return Location.objects.create(
            id=id,
            address=address,
            name=name,
            rating=rating,
            category=category,
            price_level=price_level,
            description=description
        )
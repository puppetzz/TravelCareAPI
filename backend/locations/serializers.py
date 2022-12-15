from rest_framework import serializers
from .models import Category, Location
from address.serializers import (
    AddressGetSerializer, 
    AddressCreateSerializer
)
import uuid
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from reviews.models import Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
    
class LocationSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    address = AddressGetSerializer()
    rating = serializers.SerializerMethodField()

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
    
    def get_rating(self, obj):
        id = obj.id
        if not Review.objects.filter(location__id=id).exists():
            return 0.0
        return round(Review.objects.filter(location__id=id).aggregate(Avg('rating')).get('rating__avg'), 1)

class LocationCreateSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=10)
    province = serializers.CharField(max_length=10)
    district = serializers.CharField(max_length=10)
    street_address = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
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
            category=category,
            price_level=price_level,
            description=description
        )
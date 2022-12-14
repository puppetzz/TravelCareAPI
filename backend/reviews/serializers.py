from rest_framework import serializers
from .models import TripType, Review, ImageStorage
from django.shortcuts import get_object_or_404
from users.serializers import UserReviewSerializer
from users.models import User
from locations.models import Location
import uuid

class TripTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripType
        fields = ['id', 'name', 'localized_name']
    
        
class ImageStorageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImageStorage
        fields = ['id', 'image']
    
    def validate(self, attrs):
        return attrs

class ImageCreateListSerializer(serializers.Serializer):
    review_id = serializers.CharField(max_length=10)
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        fields = ['review_id', 'images']  
    
    def create(self, validated_data):
        review_id = validated_data.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        for image in validated_data.get('images'):
            id = str(uuid.uuid4().int)[:9]
            image = ImageStorage.objects.create(id=id, review=review, image=image)
        return 'success'

class ImageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStorage
        fields = ['image']


class ReviewSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    trip_type = TripTypeSerializer()
    user = UserReviewSerializer()

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'location',
            'rating',
            'review_date',
            'trip_time',
            'trip_type',
            'title',
            'content',
            'images'
        ]
        
    def get_images(self, obj):
        id = obj.id
        if ImageStorage.objects.filter(review__id=id).exists():
            images = ImageStorage.objects.filter(review__id=id)
            serializer = ImageViewSerializer(images, many=True)
            return serializer.data

        return None


class ReviewCreateSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=10)
    location_id = serializers.CharField(max_length=10)
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    trip_type_id = serializers.CharField(max_length=10)
    trip_time = serializers.DateField()
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    
    class Meta:
        fields = [
            'user_id',
            'location_id',
            'rating',
            'trip_type_id',
            'trip_time',
            'title',
            'content',
        ]
        
    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        id = str(uuid.uuid4().int)[:9]

        user_id = validated_data.get('user_id')
        if not User.objects.filter(account__id=user_id).exists():
            raise Exception({'error': 'User not found'})
        user = User.objects.filter(account__id=user_id).first()
        
        location_id = validated_data.get('location_id')
        location = get_object_or_404(Location, id=location_id)

        trip_type_id = validated_data.get('trip_type_id')
        trip_type = get_object_or_404(TripType, id=trip_type_id)
        
        return Review.objects.create(
            id=id,
            user=user,
            location=location,
            rating=validated_data.get('rating'),
            trip_time=validated_data.get('trip_time'),
            trip_type=trip_type,
            title=validated_data.get('title'),
            content=validated_data.get('content')
        )
        

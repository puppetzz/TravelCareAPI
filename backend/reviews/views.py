from .serializers import (
    TripTypeSerializer,
    ReviewSerializer,
    ImageStorageSerializer,
    ReviewCreateSerializer,
    ImageCreateListSerializer,
)
from users.serializers import UserSerializer
from .models import TripType, Review, ImageStorage
from users.service import Service
from users.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

class TripTypeView(generics.GenericAPIView):
    serializer_class = TripTypeSerializer
    queryset = TripType.objects.all()

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if not id:
            trip_type = self.get_queryset()
            serializer = self.serializer_class(trip_type, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        trip_type = self.get_queryset().get(id=id)
        serializer = self.serializer_class(trip_type)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageStorageView(generics.GenericAPIView):
    serializer_class = ImageStorageSerializer
    queryset = ImageStorage.objects.all()
    
    def get(self, request, *args, **kwargs):
        image_id = kwargs.get('image_id')
        review_id = kwargs.get('review_id')

        if not review_id:
            if not image_id:
                images = self.get_queryset()
                serializer = self.serializer_class(images, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            image = get_object_or_404(ImageStorage, id=image_id)
            serializer = self.serializer_class(image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        images = self.get_queryset().filter(review__id=review_id)
        serializer = self.serializer_class(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
class ReviewGetView(generics.GenericAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get(self, request, *args, **kwargs):
        location_id = kwargs.get('location_id')
        review_id = kwargs.get('review_id')

        if not location_id:
            if not review_id:
                reviews = self.get_queryset()
                serializer = self.serializer_class(reviews, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            review = get_object_or_404(Review, id=review_id)
            serializer = self.serializer_class(review)
            return Response(serializer.data, status=status)
        
        reviews = self.get_queryset().filter(location__id=location_id)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReviewCreateView(generics.GenericAPIView):
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': 'Add review success.'
            },
            status=status.HTTP_200_OK)

class ImageCreateView(generics.GenericAPIView):
    queryset = ImageStorage.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ImageCreateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
                            'success': 'Add image success.'
                        },
                        status=status.HTTP_200_OK)
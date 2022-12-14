from .serializers import (
    TripTypeSerializer,
    ReviewSerializer,
    ImageStorageSerializer,
    ReviewCreateSerializer,
    ImageCreateListSerializer,
    ImageCreateSerializer,
    ReviewUpdateSerializer,
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
        user_id = kwargs.get('user_id')

        if not location_id:
            if not review_id:
                if user_id:
                    if not Review.objects.filter(user__account__id=user_id).exists():
                        return Response(
                            {
                                'error': 'User has no reviews yet.'
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    reviews = self.get_queryset().filter(user__account__id=user_id)
                    serializer = self.serializer_class(reviews, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                reviews = self.get_queryset()
                serializer = self.serializer_class(reviews, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            
            review = get_object_or_404(Review, id=review_id)
            serializer = self.serializer_class(review)
            return Response(serializer.data, status=status.HTTP_200_OK)

                
        
        reviews = self.get_queryset().filter(location__id=location_id)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReviewCreateView(generics.GenericAPIView):
    serializer_class = ReviewCreateSerializer
    queryset = Review.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        review_serializer = ReviewSerializer(review)
        return Response(review_serializer.data, status=status.HTTP_200_OK)

class ImageCreateListView(generics.GenericAPIView):
    queryset = ImageStorage.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = ImageCreateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': 'Add image success.'
            },
            status=status.HTTP_200_OK
        )

class ImageCreateView(generics.GenericAPIView):
    serializer_class = ImageCreateSerializer
    queryset = ImageStorage.objects.all() 
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'success': 'Add image success.'
            },
            status=status.HTTP_200_OK
        )
            
class ImageDeleteView(generics.GenericAPIView):
    queryset = ImageStorage.objects.all()
    
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('image_id')
        image = get_object_or_404(ImageStorage, id=id)
        image.delete()
        return Response(
            {
                'success': 'Delete Image Successfully.'
            },
            status=status.HTTP_200_OK
        )
        
class ReviewUpdateView(generics.GenericAPIView):
    serializer_class = ReviewUpdateSerializer
    queryset = Review.objects.all()

    def patch(self, request):
        id = request.data.get('id')
        review = get_object_or_404(Review, id=id)
        serializer = self.serializer_class(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
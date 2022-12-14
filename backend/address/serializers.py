from rest_framework import serializers
from .models import Country, Province, District, Address
import uuid
from django.shortcuts import get_object_or_404


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'description']


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'description']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)


class AddressCreateSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=255, write_only=True, allow_null=True, allow_blank=True)
    province = serializers.CharField(max_length=255, write_only=True, allow_null=True, allow_blank=True)
    district = serializers.CharField(max_length=255, write_only=True, allow_null=True, allow_blank=True)
    street_address = serializers.CharField(write_only=True, allow_null=True, allow_blank=True)

    class Meta:
        model = Address
        fields = [
            'country',
            'province',
            'district',
            'street_address',
        ]

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        id = str(uuid.uuid4().int)[:9]

        country_id = validated_data.pop('country')
        province_id = validated_data.pop('province')
        district_id = validated_data.pop('district')
        
        if country_id:
            if Country.objects.filter(id=country_id).exists():
                country = Country.objects.get(id=country_id)
        if province_id:
            if Province.objects.filter(id=province_id).exists():
                province = Province.objects.get(id=province_id)
        if district_id:
            if District.objects.get(id=district_id):
                district = District.objects.get(id=district_id)

        return Address.objects.create(
            id=id,
            country=country,
            province=province,
            district=district,
            **validated_data
        )


class AddressGetSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    province = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    district = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    
    class Meta:
        model = Address
        fields = [
            'country',
            'province',
            'district',
            'street_address'
        ]

class AddressDestroySerializer(serializers.Serializer):
    id = serializers.CharField(max_length=10)
    class Meta:
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    province = ProvinceSerializer()
    district = DistrictSerializer()
    class Meta:
        model = Address
        fields =[
            'country',
            'province',
            'district',
            'street_address'
        ]
        
class AddressUpdateSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=10, required=False, allow_blank=True)
    province = serializers.CharField(max_length=10, required=False, allow_blank=True) 
    district = serializers.CharField(max_length=10, required=False, allow_blank=True) 
    street_address = serializers.CharField(max_length=255, allow_blank=True)

    def validate(self, attrs):
        return attrs
    
    def update(self, instance, validated_data):
        if validated_data.get('country'):
            country = get_object_or_404(Country, id=validated_data.get('country'))
            instance.country = country
        if validated_data.get('province'):
            province = get_object_or_404(Province, id=validated_data.get('province'))
            instance.province = province
        if validated_data.get('district'):
            district = get_object_or_404(District, id=validated_data.get('district'))
            instance.district = district
        if validated_data.get('street_address'):
            instance.street_address = validated_data.get('street_address')
        instance.save()
        return instance
    
class AddressReviewSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(read_only=True, slug_field='name')
    province = serializers.SlugRelatedField(read_only=True, slug_field='name')
    district = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Address
        fields = [
            'id', 
            'country', 
            'province', 
            'district', 
            'street_address'
        ]
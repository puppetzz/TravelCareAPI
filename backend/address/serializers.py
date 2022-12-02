from rest_framework import serializers
from .models import Country, Province, District, Address
import uuid


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

    def validate(self, attrs):
        return super().validate(attrs)


class AddressSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=255, write_only=True)
    province = serializers.CharField(max_length=255, write_only=True)
    district = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Address
        fields = [
            'country',
            'province',
            'district',
            'street_address',
        ]

    def validate(self, attrs):
        country_id = attrs.get('country', '')
        province_id = attrs.get('province', '')
        district_id = attrs.get('district', '')

        if not Country.objects.filter(id=country_id).exists():
            raise Exception('country does not exist')

        if not Province.objects.filter(id=province_id).exists():
            raise Exception('province does not exist')

        if not District.objects.filter(id=district_id).exists():
            raise Exception('district does not exist')

        return attrs

    def create(self, validated_data):
        id = str(uuid.uuid4().int)[:9]

        country_id = validated_data.pop('country')
        province_id = validated_data.pop('province')
        district_id = validated_data.pop('district')

        country = Country.objects.get(id=country_id)

        province = Province.objects.get(id=province_id)

        district = District.objects.get(id=district_id)

        return Address.objects.create(
            id=id,
            country=country,
            province=province,
            district=district,
            **validated_data
        )

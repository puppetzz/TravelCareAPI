from rest_framework import serializers
from .models import User
from address.serializers import (
    AddressCreateSerializer, 
    AddressGetSerializer,
    AddressSerializer
    )
from authentication.models import Account
from address.models import Address, Country, Province, District
from django.shortcuts import get_object_or_404

class UserRegisterSerializer(serializers.ModelSerializer):
    address = AddressCreateSerializer(allow_null=True, required=False)
    id = serializers.CharField(max_length=10, required=False)
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'address'
        ]
        extra_fields = ['id',]
    
    def create(self, validated_data):
        address = validated_data.pop('address')
        if not address:
            address = None
        if hasattr(address, 'country'):
            if not address.get('country'):
                address = None
        
        id = validated_data.pop('id')
        
        if address:
            if Country.objects.filter(
                id=address['country']).exists() and Province.objects.filter(
                    id=address['province']) and District.objects.filter(
                        id=address['district']).exists():
                address_serializer = AddressCreateSerializer(data=address)
                address_serializer.is_valid(raise_exception=True)
                address = address_serializer.save()
            else:
                Account.objects.get(id=id).delete()
                raise Exception({'error': 'Address not found'})
        
        account = Account.objects.get(id=id)
        
        if address:
            return User.objects.create(account=account, address=address, **validated_data)

        return User.objects.create(account=account, **validated_data)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'email'
        ]

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    address = AddressSerializer()
    class Meta:
        model = User
        fields = [
            'account',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'profile_picture',
        ]
    
class UserUpdateSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=10)
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=11, required=False)
    country = serializers.CharField(max_length=10, required=False)
    province = serializers.CharField(max_length=10, required=False)
    district = serializers.CharField(max_length=10, required=False)
    street_address = serializers.CharField(max_length=255, required=False)
    profile_picture = serializers.ImageField(required=False)
    
    class Meta:
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'country',
            'province',
            'district',
            'profile_picture',
        ]
    
    def validate(self, attrs):
        id = attrs.get('id')
        account = get_object_or_404(Account, id=id)
        account.username = attrs.get('username')
        user = get_object_or_404(User, account=account)
        user.first_name = attrs.get('first_name')
        user.last_name = attrs.get('last_name')
        user.phone_number = attrs.get('phone_number')
        user.profile_picture = attrs.get('profile_picture')
        if attrs.get('country'):
            address = dict()
            address['country'] = attrs.get('country')
            address['province'] = attrs.get('province')
            address['district'] = attrs.get('district')
            address['street_address'] = attrs.get('street_address')
            address_serializer = AddressCreateSerializer(data=address)
            address_serializer.is_valid(raise_exception=True)
            address = address_serializer.save()
        account.save()
        user.save()
        return attrs
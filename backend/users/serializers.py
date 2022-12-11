from rest_framework import serializers
from .models import User
from address.serializers import (
    AddressCreateSerializer, 
    AddressGetSerializer,
    AddressSerializer,
    AddressUpdateSerializer
    )
from authentication.models import Account
from address.models import Address, Country, Province, District
from django.shortcuts import get_object_or_404
from django.forms import model_to_dict

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
            'email',
            'create_at',
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
    username = serializers.CharField(max_length=255, required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=11, required=False, allow_blank=True)
    country = serializers.CharField(max_length=10, required=False, allow_blank=True)
    province = serializers.CharField(max_length=10, required=False, allow_blank=True)
    district = serializers.CharField(max_length=10, required=False, allow_blank=True)
    street_address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    
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
        ]
    
    def validate(self, attrs):
        id = attrs.get('id')
        account = get_object_or_404(Account, id=id)
        if attrs.get('username'):
            account.username = attrs.get('username')
        user = get_object_or_404(User, account=account)
        if attrs.get('first_name'):
            user.first_name = attrs.get('first_name')
        if attrs.get('last_name'):
            user.last_name = attrs.get('last_name')
        if attrs.get('phone_number'):
            user.phone_number = attrs.get('phone_number')
        address = dict()
        address_id = model_to_dict(user).get('address')
        if address_id:
            address['country'] = attrs.get('country')
            address['province'] = attrs.get('province')
            address['district'] = attrs.get('district')
            address['street_address'] = attrs.get('street_address')
            if Address.objects.filter(id=address_id).exists():
                address_serializer = AddressUpdateSerializer(Address.objects.get(id=address_id), data=address)
                address_serializer.is_valid(raise_exception=True)
                address_serializer.save()
            else:
                raise Exception({'error': 'address does not exist.'})
        else:
            address_serializer = AddressCreateSerializer(data=address)
            address_serializer.is_valid(raise_exception=True)
            user.address = address_serializer.save()
        account.save()
        user.save()
        return attrs
    
class UserProfilePictureUpdateSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=10)
    profile_picture = serializers.ImageField()
    
    class Meta:
        fields = [
            'id',
            'profile_picture',
        ]
    
    def validate(self, attrs):
        account = get_object_or_404(Account, id=attrs.get('id'))
        user = get_object_or_404(User, account=account)
        if attrs.get('profile_picture'):
            user.profile_picture = attrs.get('profile_picture')
        else:
            raise Exception({'error': 'profile picture should not null.'})
        user.save()
        return attrs
    
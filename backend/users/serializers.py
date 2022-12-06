from rest_framework import serializers
from .models import User
from address.serializers import (
    AddressCreateSerializer, 
    AddressGetSerializer,
    AddressSerializer
    )
from authentication.models import Account

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
        
        if address:
            address_serializer = AddressCreateSerializer(data=address)
            address_serializer.is_valid(raise_exception=True)
            address = address_serializer.save()
        
        id = validated_data.pop('id')
        account = Account.objects.get(id=id)
        
        if address:
            return User.objects.create(account=account, address=address, **validated_data)

        return User.objects.create(account=account, **validated_data)

class AccountSerializerField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Account.objects.all()
        return queryset


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
        
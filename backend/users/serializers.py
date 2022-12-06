from rest_framework import serializers
from .models import User
from address.serializers import AddressRegisterSerializer, AddressGetSerializer
from authentication.models import Account

class UserRegisterSerializer(serializers.ModelSerializer):
    address = AddressRegisterSerializer(allow_null=True, required=False)
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
        if not address['country']:
            address = None
        
        if address:
            address_serializer = AddressRegisterSerializer(data=address)
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
    address = serializers.SerializerMethodField()
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
        
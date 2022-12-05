from rest_framework import serializers
from .models import User
from address.serializers import AddressSerializer
from authentication.models import Account


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(allow_null=True, required=False)
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
            address_serializer = AddressSerializer(data=address)
            address_serializer.is_valid(raise_exception=True)
            address_serializer.save()
        
        id = validated_data.pop('id')
        account = Account.objects.get(id=id)
        
        return User.objects.create(account=account, **validated_data)



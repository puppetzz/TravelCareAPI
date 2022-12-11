from .serializers import UserSerializer
from .models import User
from authentication.models import Account
from django.shortcuts import get_object_or_404

class Service:
    @staticmethod
    def user_to_view(user):
        user_data = user
        data = dict()
        for field in user_data['account']:
            data[field] = user_data['account'][field]
        user_data.pop('account')
        data.update(user_data)
        if data['address'] == None:
            address = {
                'country': '',
                'province': '',
                'district': '',
            }
            data['address'] = address
        return data

    @staticmethod
    def get_profile_picture(id:str):
        account = Account.objects.get(id=id)
        user = User.objects.get(account=account)
        serializer = UserSerializer(user)
        profile_picture = serializer.data.pop('profile_picture')
        return profile_picture
    
    @staticmethod
    def get_user(id:str):
        id = id
        account = get_object_or_404(Account, id=id)
        user = get_object_or_404(User, account=account)
        serializer = UserSerializer(user)
        data = Service.user_to_view(serializer.data)
        return data
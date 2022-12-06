from .serializers import UserSerializer

class Service:
    def user_to_view(user):
        user_data = user
        data = dict()
        for field in user_data['account']:
            data[field] = user_data['account'][field]
        user_data.pop('account')
        data.update(user_data)
        return data
        
        
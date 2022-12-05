from .serializers import FormRegisterSerializer

class Service:
    @staticmethod
    def convert_to_register_data(data: FormRegisterSerializer):
        if data['country']:    
            user = {
                'username': data['username'],
                'email': data['email'],
                'password': data['password'],
                'user': {
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'phone_number': data['phone_number'],
                    'address': {
                        'country': data['country'],
                        'province': data['province'],
                        'district': data['district'],
                        'street_address': data['street_address']
                    }
                },
            }
            return user
        
        user = {
                'username': data['username'],
                'email': data['email'],
                'password': data['password'],
                'user': {
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'phone_number': data['phone_number'],
                    'address': None
                },
            }
        
        return user
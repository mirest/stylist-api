import requests
from .models import User
from graphql import GraphQLError
import jwt
from datetime import datetime,timedelta
from config.default import SECRET_KEY


class Generate_User():
    token=str()
    user=object()
    user_type=''


    def __init__(self,**kwargs):
        self.token=kwargs.get('google_token')
        self.phone_number=kwargs.get('phone_number')
        self.user_type=kwargs.get('user_type')

    def generate_user(self):
        token_data=self.decode_token()
        user,msg=self.check_user(token_data)
        token=self.generate_token(user)
        return user,token,msg
    
    def decode_token(self):
        url = f'https://oauth2.googleapis.com/tokeninfo?id_token={self.token}'
        response = requests.get(url)
        if response.status_code==200:
            return response.json()
        raise GraphQLError("Invalid token Id")
    
    def check_user(self,token_data):
        user=User.objects.filter(email=token_data['email'])
        if user.exists():
            self.user=user
            msg="You have successfully logged in"
            return user.first(),msg
        new_user=self.save_new_user(token_data)
        msg="You have successfully signed up"
        return new_user,msg

    def generate_token(self, user):
        encoded_jwt = jwt.encode(
            {'username': user.email,
             'exp': datetime.now() + timedelta(days=15)},
            SECRET_KEY, algorithm='HS256').decode('utf-8')
        return encoded_jwt 

    def save_new_user(self,token_data,**kwargs):
        user_data={
            "email": token_data['email'],
            "user_type":self.user_type
        }
        user=User(**user_data)
        self.process_number(user,**kwargs)
        user.create_user()
        return user  

    def process_number(self,user,**kwargs):
        db_user=User.objects.filter(phone_number=self.phone_number)
        if db_user.exists():
            raise GraphQLError("User with the same phone number exists")
        user.phone_number=self.phone_number
        return user
        

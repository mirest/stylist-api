import jwt
from datetime import datetime, timedelta
from config.default import SECRET_KEY


class Generate_User():

    def generate_token(self, user):
        encoded_jwt = jwt.encode(
            {'username': user.email,
             'exp': datetime.now() + timedelta(days=15)},
            SECRET_KEY, algorithm='HS256').decode('utf-8')
        return encoded_jwt

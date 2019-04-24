import jwt
from graphql_jwt.exceptions import GraphQLJWTError
from graphql_jwt.middleware import JSONWebTokenMiddleware

from apps.users.models import User
from config.default import SECRET_KEY, GRAPHQL_JWT
from django.contrib.auth.models import AnonymousUser


class CustomJSONWebTokenMiddleware(JSONWebTokenMiddleware):
    authentication_header_prefix = GRAPHQL_JWT.get(
        'JWT_AUTH_HEADER_PREFIX', 'Bearer')

    def __init__(self, get_response=None):
        self.get_response = get_response

    def resolve(self, next, root, info, **kwargs):
        headers = self.get_request_headers(info.context.META)
        if headers is not None:
            auth_header_prefix = self.authentication_header_prefix.lower()

        if not headers:
            info.context.user = AnonymousUser()
            return next(root, info, **kwargs)
        headers = headers.split()

        if len(headers) == 1 or len(headers) > 2:
            msg = 'Invalid authentication. Could not decode token.'
            raise GraphQLJWTError(msg)
        prefix = headers[0]
        token = headers[1]

        if prefix.lower() != auth_header_prefix:
            msg = 'Invalid header prefix'
            raise GraphQLJWTError(msg)

        user, kwargs = self._authenticate_credentials(
            root, info, token, **kwargs)
        info.context.user = user
        return next(root, info, **kwargs)

    def _authenticate_credentials(self, root, info, token, **kwargs):
        try:
            payload = jwt.decode(token, SECRET_KEY)
        except jwt.InvalidTokenError or jwt.DecodeError:
            msg = 'Invalid authentication. Could not decode token.'
            raise GraphQLJWTError(msg)

        except jwt.ExpiredSignature:
            msg = 'Token has expired. please login again'
            raise GraphQLJWTError(msg)
        try:
            user = User.objects.get(email=payload['username'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise GraphQLJWTError(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise GraphQLJWTError(msg)
        self.user = user
        return (user, kwargs,)

    @staticmethod
    def get_request_headers(request=None):
        if request is not None:
            headers = request.get('HTTP_AUTHORIZATION')
            return headers

    def authenticate(self, request, *args, **kwargs):
        pass

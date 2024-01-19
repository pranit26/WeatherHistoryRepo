import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication,get_authorization_header
from rest_framework.exceptions import AuthenticationFailed



def generate_jwt_token(user):
    payload = {
        'user_id': user,
        'exp': datetime.utcnow() + timedelta(seconds=30),  # Token expiration time (adjust as needed)
        'iat': datetime.utcnow(),
        }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None
        try:
            token = auth_header[1].decode('utf-8')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        
        user_model = get_user_model()
        user = user_model.objects.get(id=payload['user_id'])
        return user, None

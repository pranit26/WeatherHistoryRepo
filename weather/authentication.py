from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
import pytz
import datetime
from rest_framework.authtoken.models import Token

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed("Invalid Token") 
        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted")

        utc_now = datetime.datetime.utcnow()
        utc_now=utc_now.replace(tinfo=pytz.utc)

        if token.created <utc_now-datetime.timedelta(seconds=30):
            raise AuthenticationFailed('Token has expired')

        return token.user,token
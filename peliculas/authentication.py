from rest_framework.authentication import TokenAuthentication
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


# https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py

# creo una clase para manejar la expiracion del token
class ExpiringTokenAuthentication(TokenAuthentication):

    # si el modelo no esta declarado, el modelo por defecto es Token
    token = None
    expired = False

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            user = token.user
            token.delete()
            self.expired = True
            token = self.get_model().objects.create(user=user)
        return is_expire, token

    def authenticate_credentials(self, key):
        self.token = None
        try:
            self.token = self.get_model().objects.select_related('user').get(key=key)
            token_found = True
        except: return 'token invalido', 0, True
        if token_found:
            is_expired, self.token = self.token_expire_handler(self.token)
            if not self.token.user.is_active:
                return 'usuario no activo o eliminado', 0, True
            if is_expired:
                return 'su token ha expirado', 0, True
            else:
                return self.token.user, self.token, self.expired

from .authentication import ExpiringTokenAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .api.helpers import create_response


class Authentication(object):

    user = None
    user_token_expired = False

    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                self.user_token_expired = True
                return 'token no ingresado'
            token_expire = ExpiringTokenAuthentication()
            self.user, token, self.user_token_expired = token_expire.authenticate_credentials(token)
            return self.user
        else:
            return 'no se ha especificado el token'
        # return None

    # dispatch es el metodo que toda clase de django ejecuta primero
    def dispatch(self, request, *args, **kwargs):

        user = self.get_user(request)
        if user is not None:
            if type(user) == str:
                return create_response(message='error', data=user, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return super().dispatch(request, *args, **kwargs)
        if user is None:
            return create_response(message='no se ha enviado un token', data=user, status=status.HTTP_401_UNAUTHORIZED)

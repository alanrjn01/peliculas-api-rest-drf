from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# helpers que validan si el usuario es super usuario para poder acceder a los metodos protegidos POST,DELETE,PUT,PATCH
# retornan la correspondiente accion para poder utilizarla en el archivo de vistas y sobreescribir los metodos
# de los ModelViewSets


def create_with_authorization(self, request, *args, **kwargs):
    if request.user.is_superuser:
        return ModelViewSet.create(self, request, *args, **kwargs)
    else:
        return Response({'message': "your user account don't have superuser permissions"},
                        status=status.HTTP_401_UNAUTHORIZED)


def destroy_with_authorization(request, *args, **kwargs):
    if request.user.is_superuser:
        return ModelViewSet.destroy(request, *args, **kwargs)
    else:
        return Response({'message': "your user account don't have superuser permissions"},
                        status=status.HTTP_401_UNAUTHORIZED)


def update_with_authorization(self, request, *args, **kwargs):
    if request.user.is_superuser:
        return ModelViewSet.update(self, request, *args, **kwargs)
    else:
        return Response({'message': "your user account don't have superuser permissions"},
                        status=status.HTTP_401_UNAUTHORIZED)


def partial_update_with_authorization(self, request, *args, **kwargs):
    if request.user.is_superuser:
        return ModelViewSet.partial_update(self, request, *args, **kwargs)
    else:
        return Response({'message': "your user account don't have superuser permissions"},
                        status=status.HTTP_401_UNAUTHORIZED)

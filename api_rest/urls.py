from django.contrib import admin
from django.urls import path, include
from peliculas.api.views import UserCreateApiView
# cargo las rutas de simple_jwt para generar el token y para refrescarlo
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', UserCreateApiView.as_view(), name='login'),
    path('api/', include('peliculas.api.routers'))
]

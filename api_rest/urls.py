from django.contrib import admin
from django.urls import path,include
from peliculas.api.views import Login, Logout, UserToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',Login.as_view(),name='Login'),
    path('logout/',Logout.as_view(),name='Logout'),
    path('refresh-token/',UserToken.as_view(),name='refresh'),
    path('api/', include('peliculas.api.routers')),

]

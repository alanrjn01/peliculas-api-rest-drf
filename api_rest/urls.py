from django.contrib import admin
from django.urls import path,include
from peliculas.api.views import Login, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Login.as_view(),name='Login'),
    path('logout/',Logout.as_view(),name='Logout'),
    path('api/', include('peliculas.api.routers'))
]

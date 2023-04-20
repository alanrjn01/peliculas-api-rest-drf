from rest_framework.routers import DefaultRouter
from .views import CharacterViewSet,CharacterMovieViewSet
router = DefaultRouter()

router.register(r'character', CharacterViewSet, basename='character')
router.register(r'charactermovie', CharacterMovieViewSet, basename='charactermovie')

urlpatterns = router.urls

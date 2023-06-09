from rest_framework.routers import DefaultRouter
from .views import CharacterViewSet, CharacterMovieViewSet, MovieViewSet, GenreViewSet
router = DefaultRouter()

router.register(r'character', CharacterViewSet, basename='character')
router.register(r'charactermovie', CharacterMovieViewSet, basename='charactermovie')
router.register(r'movie', MovieViewSet, basename='character')
router.register(r'genre', GenreViewSet, basename='genre')

urlpatterns = router.urls

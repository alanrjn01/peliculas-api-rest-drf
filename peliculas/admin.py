from django.contrib import admin
from .models import Movie, CharacterMovie, Character, Genre
# Register your models here.
admin.site.register(Character)
admin.site.register(CharacterMovie)
admin.site.register(Movie),
admin.site.register(Genre)
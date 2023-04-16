from rest_framework.serializers import ModelSerializer
from peliculas.models import Character, CharacterMovie, Movie, Genre


class CharacterSerializer(ModelSerializer):

    class Meta:
        model = Character
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'age' : instance.age,
            'weight' : instance.weight,
            'story' : instance.story
        }


class CharacterMovieSerializer(ModelSerializer):
    class Meta:
        model = CharacterMovie
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'character': instance.character_id.name,
            'movie': instance.movie_id.title
        }


class MovieSerializer(ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

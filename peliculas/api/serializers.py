from rest_framework.serializers import ModelSerializer
from peliculas.models import Character, CharacterMovie, Movie, Genre
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CharacterSerializer(ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'age': instance.age,
            'weight': instance.weight,
            'story': instance.story
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    # el metodo create de UserSerializer se encarga de crear una instancia de User con los datos validados
    # y hashea la contraseña, luego guarda la instancia en la base de datos
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def to_representation(self, instance):
    #     return {
    #         "name": instance.first_name
    #     }

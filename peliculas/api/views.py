from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .helpers import return_characters_list
from .serializers import CharacterSerializer, CharacterMovieSerializer


class CharacterViewSet(ModelViewSet):
    serializer_class = CharacterSerializer

    # valida que tiene que haber un token asociado al usuario que estoy intentando enviar para una clase en especifico
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def retrieve(self, request, pk):

        queryset = CharacterMovieSerializer.Meta.model.objects.filter(character_id=self.get_object().id)
        movies_list = []
        for movie in queryset:
            movies_list.append(
                {
                    'movie': movie.movie_id.title
                }
            )
        objeto = {
            'name': self.get_object().name,
            'age': self.get_object().age,
            "weight": self.get_object().weight,
            "story": self.get_object().story,
            "movies_relationated": movies_list
        }
        return Response(objeto)

    def list(self, request):

        param = request.query_params

        if param.get('name'):
            queryset = self.get_serializer().Meta.model.objects.filter(name=param.get('name'))
            if queryset:
                characters = return_characters_list(queryset)
                return Response(characters, status=status.HTTP_200_OK)

        elif param.get('age'):
            queryset = self.get_serializer().Meta.model.objects.filter(age=param.get('age'))
            characters = return_characters_list(queryset)
            if characters:
                return Response(characters, status=status.HTTP_200_OK)

        elif param.get('movie'):
            queryset = CharacterMovieSerializer.Meta.model.objects.filter(movie_id=param.get('movie'))
            character_list = []
            for movies in queryset:
                character_list.append(
                    {
                        'name': movies.character_id.name
                    }
                )
            return Response(character_list, status=status.HTTP_200_OK)
        else:
            characters = self.get_serializer(self.get_queryset(), many=True)
            print(characters)
            if characters:
                return Response(characters.data, status=status.HTTP_200_OK)
        return Response({'message': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class CharacterMovieViewSet(ModelViewSet):
    serializer_class = CharacterMovieSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

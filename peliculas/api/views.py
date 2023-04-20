from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

from .helpers import return_characters_list
from .serializers import CharacterSerializer, CharacterMovieSerializer, UserSerializer, MovieSerializer, GenreSerializer


class UserCreateApiView(CreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def post(self, request, *args, **kwargs):
        created_user = self.create(request, *args, **kwargs)
        # creo el contenido del html utilizando un template, al cual le paso variables de 'username' y 'password'
        html_content = render_to_string('email_template.html', {
            'username': created_user.data['username'],
            'password': created_user.data['password']
        })
        # creo una variable que va a tener el contenido del html sin los tags
        text_content = strip_tags(html_content)
        # creo el email
        email = EmailMultiAlternatives(
            # encabezado del correo
            'Registro exitoso',
            # contenido del correo
            text_content,
            # correo emisor
            settings.EMAIL_HOST_USER,
            # correo receptor
            [created_user.data['email']]
        )
        # indico el tipo de contenido 'text/html' para que el email lo reconozca
        email.attach_alternative(html_content, 'text/html')
        # si el mail falla muestra el error
        email.fail_silently = False
        # envio del mail
        email.send()
        return created_user


class CharacterViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_class = CharacterSerializer

    # valida que tiene que haber un token asociado al usuario que estoy intentando enviar para una clase en especifico
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def retrieve(self, request, pk, *args, **kwargs):

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
                        'character_name': movies.character_id.name
                    }
                )
            return Response(character_list, status=status.HTTP_200_OK)
        else:
            characters = self.get_serializer(self.get_queryset(), many=True)
            print(characters)
            if characters:
                return Response(characters.data, status=status.HTTP_200_OK)
        return Response({'message': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def list(self, request):
        """
        endpoint principal GET /api/movies
         * puede recibir un query param -> 'name', 'genre', 'order'
         * en caso de no recibir una query, devuelve un listado de todas las peliculas
        """
        param = request.query_params

        if param:

            if param.get('name'):
                queryset = self.get_serializer().Meta.model.objects.filter(name=param.get('name'))
                if queryset:
                    movies = return_characters_list(queryset)
                    return Response(movies, status=status.HTTP_200_OK)

            elif param.get('genre'):
                movies = self.get_serializer().Meta.model.objects.filter(genre_id=param.get('genre'))
                movies_by_genre = []
                if movies:
                    for movie in movies:
                        movies_by_genre.append({
                            'movie_title': movie.title
                        })
                    return Response(movies_by_genre, status=status.HTTP_200_OK)

            elif param.get('order') == 'ASC' or param.get('order') == 'DESC':
                movies_order_by_creation_date = list(self.get_serializer_class().Meta.model.objects.filter().order_by(
                    'release_date' if param.get('order') == 'ASC' else '-release_date').values())
                return Response(movies_order_by_creation_date, status=status.HTTP_200_OK)

            return Response({'message': 'wrong query param'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            movies = list(self.get_queryset().values('title', 'release_date'))
            return Response(movies, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        movie = self.get_serializer().Meta.model.objects.filter(id=pk).first()
        characters = CharacterMovieSerializer.Meta.model.objects.filter(movie_id=pk)
        characters_list = []
        for character in characters:
            characters_list.append({
                'character_name': character.character_id.name
            })
        json = {
            'movie': movie.title,
            'characters': characters_list
        }
        return Response(json)


class CharacterMovieViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CharacterMovieSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()


class GenreViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenreSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()
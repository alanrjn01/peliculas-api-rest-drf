from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

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
        return Response(created_user, status=status.HTTP_201_CREATED)


class CharacterViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CharacterSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def retrieve(self, request, *args, **kwargs):
        # self.get_object().id -> obtiene id sin pasar un pk

        # obtiene una lista de las peliculas donde hayan participado los personajes con el id consultado
        queryset = CharacterMovieSerializer.Meta.model.objects.filter(character_id=self.get_object().id)

        # utiliza map para retornar en cada iteracion el titulo de la pelicula del queryset
        movies_by_character_id = list(map(lambda movie: {'movie_title': movie.movie_id.title}, queryset))

        character_json = {
            'name': self.get_object().name,
            'age': self.get_object().age,
            "weight": self.get_object().weight,
            "story": self.get_object().story,
            "movie_list": movies_by_character_id or None
        }
        return Response(character_json, status=status.HTTP_200_OK)

    def list(self, request):
        """
            endpoint principal GET /api/character
            * puede recibir un query param -> 'name', 'age', 'movie'
            * en caso de no recibir una query, devuelve un listado de todos los personajes
        """
        param = request.query_params

        if param:

            if param.get('name'):
                queryset = list(self.get_serializer().Meta.model.objects.filter(name=param.get('name')).values())
                if queryset:
                    return Response(queryset, status=status.HTTP_200_OK)

            elif param.get('age'):
                queryset = list(self.get_serializer().Meta.model.objects.filter(age=param.get('age')).values())
                if queryset:
                    return Response(queryset, status=status.HTTP_200_OK)

            # en el map, retorno un objeto con la propiedad 'character' que:
            # Utiliza El Serializer de Character para utilizar el metodo to representation pasandole
            # como instancia el character del queryset
            elif param.get('movie'):
                queryset = CharacterMovieSerializer.Meta.model.objects.filter(movie_id=param.get('movie'))
                queryset_list = list(map(lambda character: {'character': CharacterSerializer().to_representation(character.
                                                            character_id)}, queryset))
                return Response(queryset_list, status=status.HTTP_200_OK)

            return Response({'message': 'wrong query param'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # se le pasa el queryset al serializer y al tener la propiedad many=true retorna un json
            characters = self.get_serializer(self.get_queryset(), many=True)
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
                # puede mejorarse con un contains o startwith
                movies = self.get_serializer().Meta.model.objects.filter(title=param.get('name'))
                if movies:
                    movies_serializer = self.get_serializer(movies, many=True)
                    return Response(movies_serializer.data, status=status.HTTP_200_OK)

            elif param.get('genre'):
                movies = self.get_serializer().Meta.model.objects.filter(genre_id=param.get('genre'))
                if movies:
                    movies_serializer = self.get_serializer(movies, many=True)
                    return Response(movies_serializer.data, status=status.HTTP_200_OK)

            elif param.get('order') == 'ASC' or param.get('order') == 'DESC':
                movies_order_by_creation_date = list(self.get_serializer_class().Meta.model.objects.filter().order_by(
                    'release_date' if param.get('order') == 'ASC' else '-release_date').values())
                return Response(movies_order_by_creation_date, status=status.HTTP_200_OK)

            return Response({'message': 'wrong query param'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            movies = self.get_serializer(self.get_queryset(), many=True)
            return Response(movies.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Busca en la tabla de CharacterMovie la pelicula por id
        crea una lista donde ingreso todos los personas como objetos serializados del queryset movie
        para obtener el nombre de la pelicula utilizo el metodo first() del queryset 'movie' y obtengo su id y lo
        convierto a string
        """

        movie = CharacterMovieSerializer.Meta.model.objects.filter(movie_id=self.get_object())

        characters_list = list(map(lambda character: CharacterSerializer().to_representation(
                                                        character.character_id), movie))
        json = {
            'movie': str(movie.first().movie_id),
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

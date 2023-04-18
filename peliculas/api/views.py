from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CharacterSerializer, CharacterMovieSerializer, MovieSerializer, UserTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from .helpers import delete_sessions, create_response_with_token, return_characters_list
from peliculas.authentication_mixins import Authentication


class CharacterViewSet(Authentication, ModelViewSet):
    serializer_class = CharacterSerializer

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
            if characters:
                return Response(characters.data, status=status.HTTP_200_OK)
        return Response({'message': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class CharacterMovieViewSet(ModelViewSet):
    serializer_class = CharacterMovieSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        # usa el AuthTokenSerializer para crear un serializer con la data del request
        login_serializer = self.serializer_class(data=request.data, context={'request': request})
        # comprueba si es valido al pasarla por el serializador
        if login_serializer.is_valid():
            # obtiene el user del loginserializer validado
            user = login_serializer.validated_data['user']
            # comprueba si el usuario esta activo
            if user.is_active:
                # obtiene en la tabla de Token la instancia donde el usuario sea igual al usuario del request
                token, created = Token.objects.get_or_create(user=user)
                # utilizo el serializador de usuario
                user_serializer = UserTokenSerializer(user)
                # si el token para ese usuario no existia y fue creado:
                if created:
                    create_response_with_token(token.key, user_serializer.data,
                                               'token creado por primera vez', status.HTTP_201_CREATED)
                # si el token ya existia, se elimina la sesion al mismo y el token y se crea un token nuevo
                else:
                    if delete_sessions(user, Session):
                        token.delete()
                        token, created = Token.objects.get_or_create(user=user)
                        return create_response_with_token(token.key, user_serializer.data,
                                                          'el token fue eliminado y se le asigno uno nuevo',
                                                          status.HTTP_201_CREATED)
            # si el usuario no esta activo:
            else:
                return Response({'message:''el usuario no se encuentra activo'})
        # inicio de sesion incorrecto
        return Response({'message': 'inicio de sesion incorrecto'}, status=status.HTTP_200_OK)


class Logout(APIView):

    def post(self, request, *args, **kwargs):

        # recibe la key por un formdata y la busca en la base de datos
        try:
            request_token = request.data['key']
            token = Token.objects.filter(key=request_token).first()
            # si encuentra la key el usuario relacionado con la misma lo elimina y su sesion tambien
            if token:
                user = token.user
                delete_sessions(user, Session)
                # tambien se elimina el token
                token.delete()
                session_message = 'sesisones de usuario eliminadas'
                token_message = 'token eliminado'
                return Response({
                    'session_message': session_message,
                    'token_message': token_message
                }, status=status.HTTP_200_OK)
            return Response({'message': 'no se ha encontrado el token especificado'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': 'token invalido'}, status=status.HTTP_400_BAD_REQUEST)


class UserToken(APIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(
                user=UserTokenSerializer().Meta.model.objects.filter(username=username).first())
            return Response({
                'token': user_token.key
            })
        except:
            return Response({
                'error': 'credenciales incorrectas o inexistentes'
            }, status.HTTP_400_BAD_REQUEST)

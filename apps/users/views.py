# from rest_framework import status
# from rest_framework.generics import RetrieveUpdateAPIView
# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.views import APIView
# from rest_framework.response import Response
#
#
# from apps.products.serializers import RegistrationSerializer
# from apps.users.renderers import UserJSONRenderer
# from apps.users.serializers import LoginSerializer, UserSerializer
#
#
# class LoginAPIView(APIView):
#     permission_classes = [AllowAny, ]
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         user = request.data
#
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class RegistrationAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = RegistrationSerializer
#     # @schema_auto_view()
#
#     def post(self, request):
#         request_body = request.data
#         serializer = self.serializer_class(data=request_body)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = UserSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         serializer = self.serializer_class(request.user)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def update(self, request, *args, **kwargs):
#         serializer_data = request.data.get('user', {})
#
#         serializer = self.serializer_class(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer

User = get_user_model()


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomAuthToken(ObtainAuthToken):
    serializer_class = UserAuthSerializer


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        srz = UserSerializer(data=request.data)
        if srz.is_valid():
            srz.save()
            return Response({'response': 'Registered',
                             'email': srz.data['email'],
                             'username': srz.data['username'],
                             'password': srz.data['password']})


@api_view(['POST'])
@permission_classes((AllowAny,))
def customer_login(request):
    data = request.data

   # print(User.objects.values_list('email', flat=True))

    try:
        email = data['email']
        password = data['password']
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email, password=password)
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        user_token = user.auth_token.key
    except:
        user_token = Token.objects.create(user=user)

    data = {'token': user_token}
    return Response(data=data, status=status.HTTP_200_OK)

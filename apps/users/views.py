from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer, UserAuthSerializer

User = get_user_model()


class CustomAuthToken(ObtainAuthToken):
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'email': user.email, 'usename': user.username,
                         'first_name': user.first_name, 'last_name': user.last_name, 'password': user.password,
                         'date_of_birth': user.date_of_birth, 'phone_number': user.phone_number})


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        srz = UserSerializer(data=request.data)
        if srz.is_valid():
            srz.save()
            return Response({'response': "Registered",
                             'email': srz.data['email'],
                             'username': srz.data['username'],
                             'last_name': srz.data['last_name'],
                             'phone_number': srz.data['phone_number'],
                             'first_name': srz.data['first_name'],
                             'date_of_birth': srz.data['date_of_birth'],
                             'password': srz.data['password']})


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        serializer_data = request.data.get(id=pk)
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK, )


class UsersListAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

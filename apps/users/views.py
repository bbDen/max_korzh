from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import UserSerializer, UserAuthSerializer

User = get_user_model()


class CustomAuthToken(ObtainAuthToken, APIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        srz = UserAuthSerializer(data=request.data)
        return Response(srz.data)


class RegisterUser(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        srz = UserSerializer(data=request.data)
        if srz.is_valid():
            print(srz.validated_data)
            srz.save()
            return Response(srz.data, {'Response': 'Registered'})



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

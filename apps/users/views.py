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

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
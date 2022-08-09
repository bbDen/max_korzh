import random

from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import OrderItem, Order
from apps.users.serializers import (
    UserSerializer, UserAuthSerializer, ChangePasswordSerializer,
    RegistrationSerializer, OrderItemSerializer)
from apps.users.services import send_email_to_user

User = get_user_model()


class CustomAuthToken(ObtainAuthToken):
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'email': user.email, 'username': user.username,
                         'first_name': user.first_name, 'last_name': user.last_name, 'password': user.password,
                         'date_of_birth': user.date_of_birth, 'phone_number': user.phone_number})


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'response': "Password changed"})


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        srz = RegistrationSerializer(data=request.data)

        srz.is_valid(raise_exception=True)
        user = srz.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'response': "Registered",
                         'username': srz.data['username'],
                         'email': srz.data['email'],
                         'first_name': srz.data['first_name'],
                         'last_name': srz.data['last_name'],
                         'phone_number': srz.data['phone_number'],
                         'date_of_birth': srz.data['date_of_birth'],
                         'token': token.key}
                        )


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK, )


class OrderItemView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def post(self, request, *args, **kwargs):
        """
        {
        "address": "isanova", "city": "Bihskek",
         "cart": [{"id": 12, "size": "XL"}, {"id": 32, "size": "XL"}]
         "totalPrice": 23456789
         }
        """
        srz = OrderItemSerializer(data=request.data)
        srz.is_valid(raise_exception=True)
        order = Order.objects.create(address=srz.validated_data['address'],
                                     city=srz.validated_data['city'],
                                     country=srz.validated_data['country'],
                                     postcode=srz.validated_data['postcode'],
                                     customer=srz.validated_data['customer'])
        for item in srz.validated_data['cart']:
            OrderItem.objects.create(order=order, product=item['product'])

        total_price = request.data['totalPrice']

        message = f'Здравствуйте! Спасибо, что заказали товар у нас. Номер вашего заказа ' \
                  f'{id(order)}.Сумма заказа {total_price}.' \
                  f'Оплата прошла успешно, ожидайте заказ! Срок доставки' \
                  f' от 15 до 30 дней. '
        send_email_to_user(email=srz.validated_data['customer'], message=message)
        return Response(srz.data, status=status.HTTP_200_OK)


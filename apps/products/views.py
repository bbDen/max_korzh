from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, generics, filters
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from apps.products.models import Product, ProductCategory, Comment
from apps.products.serializers import ProductSerializer, ProductCategoriesSerializer, CommentSerializer
from apps.users.models import Order
from apps.users.serializers import OrderSerializer
from apps.users.services import send_email_to_user

User = get_user_model()


class ProductsListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'category']
    serializer_class = ProductSerializer
    search_fields = ['title']
    ordering_fields = ['price', 'title', 'id', 'created_at']
    queryset = Product.objects.all()

    def post(self, request):
        request_body = request.data
        srz = ProductSerializer(data=request_body)
        if srz.is_valid():
            srz.save()
            return Response(srz.data, status=status.HTTP_201_CREATED)
        else:
            return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        srz = ProductSerializer(product, many=False)
        return Response(srz.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return JsonResponse({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ProductCategoriesListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'products']
    serializer_class = ProductCategoriesSerializer
    queryset = ProductCategory.objects.all()

    def post(self, request):
        request_body = request.data
        srz = ProductCategoriesSerializer(data=request_body)
        if srz.is_valid():
            srz.save()
            return Response(srz.data, status=status.HTTP_201_CREATED)
        else:
            return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCategoriesAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price', 'title']

    def get(self, request, pk):
        sort_by = request.GET.get('ordering', None)
        try:
            category = ProductCategory.objects.get(id=pk)
        except ProductCategory.DoesNotExist:
            return Response({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        srz = ProductCategoriesSerializer(category, many=False,
                                          context={'order_value': sort_by})
        return Response(srz.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = ProductCategory.objects.get(id=pk)
        except ProductCategory.DoesNotExist:
            return JsonResponse({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post']
    serializer_class = CommentSerializer
    search_fields = ['post']
    ordering_fields = ['id', 'created_at']
    queryset = Comment.objects.all()

    def post(self, request):
        request_body = request.data
        srz = CommentSerializer(data=request_body)
        if srz.is_valid():
            srz.save()
            return Response(srz.data, status=status.HTTP_201_CREATED)
        else:
            return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            product = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({'msg': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        srz = CommentSerializer(product, many=False)
        return Response(srz.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return JsonResponse({'msg': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class OrdersListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def post(self, request):
        srz = OrderSerializer(data=request.data, context={'request': request})
        srz.is_valid(raise_exception=True)
        srz.save()
        message = 'Hello world'
        send_email_to_user(email=srz.validated_data['customer'], message=message)
        return Response(srz.data, status=status.HTTP_200_OK)

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from apps.products.models import Products, ProductCategories
from apps.products.serializers import ProductSerializer, ProductCategoriesSerializer

User = get_user_model()


class ProductsListAPIView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'category']
    serializer_class = ProductSerializer
    search_fields = ['title', 'category']
    ordering_fields = ['price', 'title']
    queryset = Products.objects.all()
    def post(self, request):
        print(request.data)
        request_body = request.data
        new_product = Products.objects.create(title=request_body['title'],
                                              category=request_body['category'],
                                              price=request_body['price'],
                                              description=request_body['description'])
        srz = ProductSerializer(new_product, many=False)
        return Response(srz.data, status=status.HTTP_201_CREATED)


class ProductRetrieveAPIView(APIView):
    def get(self, request, pk):
        try:
            product = Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return Response({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        srz = ProductSerializer(product, many=False)
        return Response(srz.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return JsonResponse({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ProductCategoriesListAPIView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    serializer_class = ProductCategoriesSerializer
    queryset = ProductCategories.objects.all()

    def post(self, request):
        request_body = request.data
        new_product = ProductCategories.objects.create(title=request_body['title'],
                                                       )
        srz = ProductCategoriesSerializer(new_product, many=False)
        return Response(srz.data, status=status.HTTP_201_CREATED)


class ProductCategoriesAPIView(APIView):
    def get(self, request, pk):
        try:
            product = ProductCategories.objects.get(id=pk)
        except ProductCategories.DoesNotExist:
            return Response({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        srz = ProductSerializer(product, many=False)
        return Response(srz.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            product = ProductCategories.objects.get(id=pk)
        except ProductCategories.DoesNotExist:
            return JsonResponse({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


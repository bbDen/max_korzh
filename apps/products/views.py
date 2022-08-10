
from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, generics, filters
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from apps.products.models import Product, ProductCategory
from apps.products.serializers import ProductSerializer, ProductCategoriesSerializer



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
    queryset = Product.objects.all()

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
    serializer_class = ProductCategoriesSerializer
    queryset = ProductCategory.objects.all()

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

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from apps.music.views import MusicListAPIView
from apps.products.views import ProductsListAPIView, ProductCategoriesAPIView, ProductRetrieveAPIView, \
    ProductCategoriesListAPIView, CommentListAPIView, CommentRetrieveAPIView
from apps.users.views import CustomAuthToken, RegisterUser, UserRetrieveUpdateAPIView, UsersListAPIView, \
    ChangePasswordView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/products/', ProductsListAPIView.as_view()),
    path('api/v1/products/<int:pk>/', ProductRetrieveAPIView.as_view()),
    path('api/v1/categories/', ProductCategoriesListAPIView.as_view()),
    path('api/v1/categories/<int:pk>/', ProductCategoriesAPIView.as_view()),
    path('api/v1/comments/', CommentListAPIView.as_view()),
    path('api/v1/comments/<int:pk>', CommentRetrieveAPIView.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api/v1/registration/', RegisterUser.as_view()),
    path('api/v1/users/', UserRetrieveUpdateAPIView.as_view()),
    path('api/v1/user/', UsersListAPIView.as_view()),
    path('api/v1/changepassword/', ChangePasswordView.as_view()),
    path('api/v1/music/', MusicListAPIView.as_view())
]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    urlpatterns += re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})

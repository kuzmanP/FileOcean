from django.contrib import admin
from django.urls import path, include
from .views import UserAPIView,UserID_APIView,UniqueUserAPIView,ProfileAPI
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="FileOcean API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)


urlpatterns = [
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path("users/", UserAPIView.as_view(), name="users"),
    path("users/<int:id>", UserID_APIView.as_view(), name="users_id"),
    path("user/<int:id>", UniqueUserAPIView.as_view(), name="unique_user"),
    path("profile/<int:id>", ProfileAPI.as_view(), name="profile")
]
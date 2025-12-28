from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserCreateAPIView.as_view(), name="user-create"),
    path("list/", views.UserListAPIView.as_view(), name="user-list"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]

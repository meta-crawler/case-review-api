from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .views import RegisterView, GetUserDataView, GetUserListView


def authenticated_view(view_class):
    return permission_classes([IsAuthenticated])(view_class)


urlpatterns = [
    path('account/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/register', RegisterView.as_view(), name="sign_up"),
    path('account/me', authenticated_view(GetUserDataView).as_view()),
    path('user-list', authenticated_view(GetUserListView).as_view()),
]

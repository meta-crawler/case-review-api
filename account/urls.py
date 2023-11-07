from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .views import RegisterView, GetUserDataView


def authenticated_view(view_class):
    return permission_classes([IsAuthenticated])(view_class)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('me/', authenticated_view(GetUserDataView).as_view()),
]

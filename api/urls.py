from django.urls import path
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .views import AlertApiView, CaseReviewApiView, CaseApiView, CommentApiView


def authenticated_view(view_class):
    return permission_classes([IsAuthenticated])(view_class)


urlpatterns = [
    path('alert', authenticated_view(AlertApiView.as_view())),
    path('case-review', authenticated_view(CaseReviewApiView.as_view())),
    path('case', authenticated_view(CaseApiView.as_view())),
    path('comment', authenticated_view(CommentApiView.as_view()))
]

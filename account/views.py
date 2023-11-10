from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AuthSerializer, UserSerializer
from .models import UserData


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class GetUserDataView(APIView):
    model = UserData
    serializer_class = UserSerializer

    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )


class GetUserListView(APIView):
    def get(self, request):
        user_queryset = UserData.objects.all()
        users = UserSerializer(user_queryset, many=True)

        return Response(
            {
                'data': users.data
            },
            status=status.HTTP_200_OK
        )

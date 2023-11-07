from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Alert, AlertType
from .serializers import AlertSerializer


# Create your views here.
class AlertApiView(generics.CreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get(self, request, *args, **kwargs):
        alert_id = request.GET.get('id')
        try:
            if alert_id is None or alert_id == '':
                queryset = Alert.objects.select_related('alert_type').all().order_by('-created_at')
            else:
                try:
                    queryset = Alert.objects.select_related('alert_type').filter(id=alert_id)
                except Alert.DoesNotExist:
                    return Response({'Message': 'Alert not found. Please provide the correct alert_id'},
                                    status=status.HTTP_404_NOT_FOUND)

            serializer = AlertSerializer(queryset, many=True)

            return Response(
                {
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'Message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        serializer = AlertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            alert_type_id = serializer.validated_data.pop('alert_type', None)
            alert_type_instance = AlertType.objects.get(id=alert_type_id)
            serializer.validated_data['alert_type'] = alert_type_instance
            alert = serializer.save()
            alert_obj = AlertSerializer(alert).data

            return Response(
                {
                    'data': alert_obj,
                },
                status=status.HTTP_201_CREATED
            )
        except AlertType.DoesNotExist:
            return Response({'Message': 'AlertType not found. Please provide the correct alert_type_id'},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        alert_id = request.GET.get('id')

        if alert_id is None:
            raise ValidationError({'Message': 'Please provide the alert_id in the request data.'})

        try:
            instance = Alert.objects.get(id=alert_id)
            serializer = AlertSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                alert_type_id = serializer.validated_data.pop('alert_type', None)
                alert_type_instance = AlertType.objects.get(id=alert_type_id)
                serializer.validated_data['alert_type'] = alert_type_instance
                alert = serializer.save()
                alert_obj = AlertSerializer(alert).data

                return Response(
                    {
                        'data': alert_obj,
                    },
                    status=status.HTTP_201_CREATED
                )
            except AlertType.DoesNotExist:
                return Response({'Message': 'AlertType not found. Please provide the correct alert_type_id'},
                                status=status.HTTP_404_NOT_FOUND)
        except Alert.DoesNotExist:
            return Response({'Message': 'Alert not found. Please provide the correct alert_id'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        alert_id = request.GET.get('id')

        try:
            instance = Alert.objects.get(id=alert_id)
            instance.delete()
            return Response({'Message': 'Alert has been successfully deleted.'},
                            status=status.HTTP_204_NO_CONTENT)
        except Alert.DoesNotExist:
            return Response({'Message': 'Alert not found.'}, status=status.HTTP_404_NOT_FOUND)

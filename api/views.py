from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from account.models import UserData
from .models import Alert, AlertType, CaseReview, CaseReviewStatus, Case, CaseStatus, Comment
from .serializers import AlertSerializer, CaseReviewSerializer, CaseSerializer, CommentSerializer, \
    CommentByCaseSerializer


# Create your views here.
class AlertApiView(CreateAPIView):
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

        if alert_id is None or alert_id == '':
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


class CaseReviewApiView(CreateAPIView):
    queryset = CaseReview.objects.all()
    serializer_class = CaseReviewSerializer

    def get(self, request, *args, **kwargs):
        case_review_id = request.GET.get('id')
        try:
            if case_review_id is None or case_review_id == '':
                queryset = CaseReview.objects.select_related('authority', 'assigner', 'status').all().order_by(
                    '-created_at')
            else:
                queryset = CaseReview.objects.select_related('authority', 'assigner', 'status').filter(
                    id=case_review_id)

            serializer = CaseReviewSerializer(queryset, many=True)

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
        serializer = CaseReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            status_id = serializer.validated_data.pop('status', None)
            status_instance = CaseReviewStatus.objects.get(id=status_id)
            serializer.validated_data['status'] = status_instance

            authority_id = serializer.validated_data.pop('authority', None)
            authority_instance = UserData.objects.get(id=authority_id)
            serializer.validated_data['authority'] = authority_instance

            assigner_id = serializer.validated_data.pop('assigner', None)
            assigner_instance = UserData.objects.get(id=assigner_id)
            serializer.validated_data['assigner'] = assigner_instance

            case_review = serializer.save()
            case_review_obj = CaseReviewSerializer(case_review).data

            return Response(
                {
                    'data': case_review_obj,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'Message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, *args, **kwargs):
        case_review_id = request.GET.get('id')

        if case_review_id is None or case_review_id == '':
            raise ValidationError({'Message': 'Please provide the case_review_id in the request data.'})

        try:
            instance = CaseReview.objects.get(id=case_review_id)
            serializer = CaseReviewSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                status_id = serializer.validated_data.pop('status', None)
                status_instance = CaseReviewStatus.objects.get(id=status_id)
                serializer.validated_data['status'] = status_instance

                authority_id = serializer.validated_data.pop('authority', None)
                authority_instance = UserData.objects.get(id=authority_id)
                serializer.validated_data['authority'] = authority_instance

                assigner_id = serializer.validated_data.pop('assigner', None)
                assigner_instance = UserData.objects.get(id=assigner_id)
                serializer.validated_data['assigner'] = assigner_instance

                case_review = serializer.save()
                case_review_obj = CaseReviewSerializer(case_review).data

                return Response(
                    {
                        'data': case_review_obj,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {
                        'Message': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except CaseReview.DoesNotExist:
            return Response({'Message': 'CaseReview not found. Please provide the correct case_review_id'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        case_review_id = request.GET.get('id')

        try:
            instance = CaseReview.objects.get(id=case_review_id)
            instance.delete()
            return Response({'Message': 'CaseReview has been successfully deleted.'},
                            status=status.HTTP_204_NO_CONTENT)
        except CaseReview.DoesNotExist:
            return Response({'Message': 'CaseReview not found.'}, status=status.HTTP_404_NOT_FOUND)


class CaseApiView(CreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def get(self, request, *args, **kwargs):
        case_id = request.GET.get('id')
        try:
            if case_id is None or case_id == '':
                queryset = Case.objects.select_related('alert', 'authority', 'status', 'case_review').all().order_by(
                    '-created_at')
            else:
                queryset = Case.objects.select_related('alert', 'authority', 'status', 'case_review').filter(
                    id=case_id)

            serializer = CaseSerializer(queryset, many=True)

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
        serializer = CaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            alert_id = serializer.validated_data.pop('alert', None)
            alert_instance = Alert.objects.get(id=alert_id)
            serializer.validated_data['alert'] = alert_instance

            authority_id = serializer.validated_data.pop('authority', None)
            authority_instance = UserData.objects.get(id=authority_id)
            serializer.validated_data['authority'] = authority_instance

            status_id = serializer.validated_data.pop('status', None)
            status_instance = CaseStatus.objects.get(id=status_id)
            serializer.validated_data['status'] = status_instance

            case_review_id = serializer.validated_data.pop('case_review', None)
            case_review_instance = CaseReview.objects.get(id=case_review_id)
            serializer.validated_data['case_review'] = case_review_instance

            case = serializer.save()
            case_obj = CaseSerializer(case).data

            return Response(
                {
                    'data': case_obj,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'Message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, *args, **kwargs):
        case_id = request.GET.get('id')

        if case_id is None or case_id == '':
            raise ValidationError({'Message': 'Please provide the case_id in the request data.'})

        try:
            instance = Case.objects.get(id=case_id)
            serializer = CaseSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                alert_id = serializer.validated_data.pop('alert', None)
                alert_instance = Alert.objects.get(id=alert_id)
                serializer.validated_data['alert'] = alert_instance

                authority_id = serializer.validated_data.pop('authority', None)
                authority_instance = UserData.objects.get(id=authority_id)
                serializer.validated_data['authority'] = authority_instance

                status_id = serializer.validated_data.pop('status', None)
                status_instance = CaseStatus.objects.get(id=status_id)
                serializer.validated_data['status'] = status_instance

                case_review_id = serializer.validated_data.pop('case_review', None)
                case_review_instance = CaseReview.objects.get(id=case_review_id)
                serializer.validated_data['case_review'] = case_review_instance

                case = serializer.save()
                case_obj = CaseSerializer(case).data

                return Response(
                    {
                        'data': case_obj,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {
                        'Message': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Case.DoesNotExist:
            return Response({'Message': 'Case not found. Please provide the correct case_id'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        case_id = request.GET.get('id')

        try:
            instance = Case.objects.get(id=case_id)
            instance.delete()
            return Response({'Message': 'Case has been successfully deleted.'},
                            status=status.HTTP_204_NO_CONTENT)
        except Case.DoesNotExist:
            return Response({'Message': 'Case not found.'}, status=status.HTTP_404_NOT_FOUND)


class CommentApiView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        comment_id = request.GET.get('id')
        try:
            if comment_id is None or comment_id == '':
                queryset = Comment.objects.select_related('author', 'case').all().order_by('-created_at')
            else:
                queryset = Comment.objects.select_related('author', 'case').filter(id=comment_id)

            serializer = CommentSerializer(queryset, many=True)

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
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            author_id = serializer.validated_data.pop('author', None)
            author_instance = UserData.objects.get(id=author_id)
            serializer.validated_data['author'] = author_instance

            case_id = serializer.validated_data.pop('case', None)
            case_instance = Case.objects.get(id=case_id)
            serializer.validated_data['case'] = case_instance

            comment = serializer.save()
            comment_obj = CommentSerializer(comment).data

            return Response(
                {
                    'data': comment_obj,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'Message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, *args, **kwargs):
        comment_id = request.GET.get('id')

        if comment_id is None or comment_id == '':
            raise ValidationError({'Message': 'Please provide the comment_id in the request data.'})

        try:
            instance = Comment.objects.get(id=comment_id)
            serializer = CommentSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                author_id = serializer.validated_data.pop('author', None)
                author_instance = UserData.objects.get(id=author_id)
                serializer.validated_data['author'] = author_instance

                case_id = serializer.validated_data.pop('case', None)
                case_instance = Case.objects.get(id=case_id)
                serializer.validated_data['case'] = case_instance

                comment = serializer.save()
                comment_obj = CommentSerializer(comment).data

                return Response(
                    {
                        'data': comment_obj,
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {
                        'Message': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Comment.DoesNotExist:
            return Response({'Message': 'Comment not found. Please provide the correct comment_id'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        comment_id = request.GET.get('id')

        try:
            instance = Comment.objects.get(id=comment_id)
            instance.delete()
            return Response({'Message': 'Comment has been successfully deleted.'},
                            status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'Message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)


class GetCommentsByCase(GenericAPIView):
    def get(self, request):
        case_id = request.GET.get('case_id')
        try:
            queryset = Comment.objects.filter(case_id=case_id)
            comment_serializer = CommentByCaseSerializer(queryset, many=True)
            comment_data = comment_serializer.data

            return Response({'data': comment_data}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'Message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)


class GetCasesByAuthority(GenericAPIView):
    def get(self, request):
        authority_id = request.GET.get('authority_id')
        try:
            if authority_id is None or authority_id == '-1':
                queryset = Case.objects.all()
            else:
                queryset = Case.objects.filter(authority_id=authority_id)
            case_serializer = CaseSerializer(queryset, many=True)
            case_data = case_serializer.data

            return Response({'data': case_data}, status=status.HTTP_200_OK)

        except Case.DoesNotExist:
            return Response({'Message': 'Case not found.'}, status=status.HTTP_404_NOT_FOUND)

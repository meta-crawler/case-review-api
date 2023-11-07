from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from account.serializers import UserSerializer
from .models import AlertType, Alert, CaseStatus, Case, CaseReviewStatus, CaseReview, Comment


class AlertTypeSerializer(ModelSerializer):
    class Meta:
        model = AlertType
        fields = '__all__'


class CaseStatusSerializer(ModelSerializer):
    class Meta:
        model = CaseStatus
        fields = '__all__'


class CaseReviewStatusSerializer(ModelSerializer):
    class Meta:
        model = CaseReviewStatus
        fields = '__all__'


class AlertSerializer(ModelSerializer):
    alert_type = serializers.IntegerField(write_only=True)

    class Meta:
        model = Alert
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['alert_type'] = AlertTypeSerializer(instance.alert_type).data

        return representation


class CaseReviewSerializer(ModelSerializer):
    authority = serializers.IntegerField(write_only=True)
    assigner = serializers.IntegerField(write_only=True)
    status = serializers.IntegerField(write_only=True)

    class Meta:
        model = CaseReview
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['authority'] = UserSerializer(instance.authority).data
        representation['assigner'] = UserSerializer(instance.assigner).data
        representation['status'] = CaseReviewStatusSerializer(instance.status).data

        return representation


class CaseSerializer(ModelSerializer):
    authority = serializers.IntegerField(write_only=True)
    alert = serializers.IntegerField(write_only=True)
    case_review = serializers.IntegerField(write_only=True)

    class Meta:
        model = Case
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['authority'] = UserSerializer(instance.authority).data
        representation['alert'] = AlertSerializer(instance.alert).data
        representation['case_review'] = CaseReviewSerializer(instance.case_review).data

        return representation


class CommentSerializer(ModelSerializer):
    alert = serializers.IntegerField(write_only=True)
    case = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author).data
        representation['case'] = CaseSerializer(instance.case).data

        return representation

from rest_framework import serializers
from .models import UserData, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'], name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = UserData

        fields = (
            'id',
            'email',
            'name',
            'date_joined',
            'password',
            'last_login',
            'is_admin',
            'is_staff',
            'is_active',
            'is_superuser',
            'team',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["team"] = TeamSerializer(instance.team).data

        return representation

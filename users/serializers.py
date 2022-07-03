from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token

from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise AssertionError

        token = Token.objects.get_or_create(user=user)[0]

        return {"token": token.key}


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


from rest_framework import serializers

from .models import Genre


class GenreSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=127)

    def create(self, validated_data):
        genre = Genre.objects.create(**validated_data)

        return genre

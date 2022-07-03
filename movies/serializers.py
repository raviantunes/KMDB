from rest_framework import serializers

from genres.serializers import GenreSerializer

from genres.models import Genre
from .models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data):

        genres = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for genre in genres:
            current_genre = Genre.objects.get_or_create(**genre)
            movie.genres.add(current_genre[0])

        return movie

    def update(self, instance: Movie, validated_data):
        genres = validated_data.pop("genres", None)

        if genres:
            for genre in genres:
                current_genre = Genre.objects.get_or_create(**genre)
                instance.genres.add(current_genre[0])

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class ReviewMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id']

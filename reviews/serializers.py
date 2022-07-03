from rest_framework import serializers
from movies.serializers import ReviewMovieSerializer

from users.serializers import CriticSerializer

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)
    movie_id = ReviewMovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'stars', 'review', 'spoilers',
                  'movie_id', 'critic', 'recomendation']
        read_only_fields = ['id', 'movie_id', 'critic']
        depth = 1

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)

        return review

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

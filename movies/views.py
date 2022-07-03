from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Movie
from .serializers import MovieSerializer


class MovieView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request):

        if request.user.is_superuser == 1:
            pass
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_401_UNAUTHORIZED)

        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieViewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"message": "This movie has not been registered"}, status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie)

        return Response(serializer.data)

    def patch(self, request, movie_id):
        if request.user.is_superuser == 1:
            pass
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_401_UNAUTHORIZED)
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"message": "This movie has not been registered"}, status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, movie_id):
        if request.user.is_superuser == 1:
            pass
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_401_UNAUTHORIZED)
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"message": "This movie has not been registered"}, status.HTTP_404_NOT_FOUND)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

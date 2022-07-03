from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Review
from movies.models import Movie

from .serializers import ReviewSerializer


class ReviewView(APIView, PageNumberPagination):

    def get(self, request):
        reviews = Review.objects.all()
        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class MovieReviewDetailView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"message": "This movie has not been registered"}, status.HTTP_404_NOT_FOUND)

        reviews = movie.reviews.all()
        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"message": "This movie has not been registered"}, status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(movie_id=movie, critic=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class DeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response({"message": "This review has not been registered"}, status.HTTP_404_NOT_FOUND)

        if request.user.is_superuser == 1 or review in request.user.reviews:
            pass
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_401_UNAUTHORIZED)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

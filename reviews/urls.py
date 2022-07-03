from django.urls import path

from .views import DeleteReviewView, ReviewView, MovieReviewDetailView

urlpatterns = [
    path('reviews/', ReviewView.as_view()),
    path('movies/<int:movie_id>/reviews/', MovieReviewDetailView.as_view()),
    path('reviews/<int:review_id>/', DeleteReviewView.as_view())
]

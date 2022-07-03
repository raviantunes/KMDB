from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class RecomendationReview(models.TextChoices):
    MUST_WATCH = ("MW", "Must Watch")
    SHOULD_WATCH = ("SW", "Should Watch")
    AVOID_WATCH = ("AW", "Avoid Watch")
    NO_OPINION = ("NO", "No Opinion")


class Review(models.Model):
    stars = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(
        max_length=50, choices=RecomendationReview.choices, default=RecomendationReview.NO_OPINION)

    movie_id = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="reviews")
    critic = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews")

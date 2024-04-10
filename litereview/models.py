from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    """Registered website user."""

    username = models.CharField(max_length=15, unique=True)

    # email = models.EmailField(unique=True)

    follows = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="UserFollows",
        related_name="followed_user",
        verbose_name="Abonnements",
    )

    def __str__(self):
        return self.username


class Ticket(models.Model):
    # tickets crees
    objects = None
    title = models.CharField(max_length=128, verbose_name="Titre")

    description = models.TextField(max_length=2048, blank=True)

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    image = models.ImageField(null=True, blank=True, upload_to="tickets")

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    objects = None
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note",
    )
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.CharField(max_length=8192, blank=True, verbose_name="Commentaire")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    objects = None
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )


class UserBlock(models.Model):
    objects = None
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blocking"
    )
    blocked_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blocked_by"
    )

    class Meta:
        # ensures we don't get multiple UserBlock instances
        # for unique user-user_followed pairs
        unique_together = (
            "user",
            "blocked_user",
        )

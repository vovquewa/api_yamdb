import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    GROUP_CHOICES = (
        ('USER', 'user'),
        ('MODERATOR', 'moderator'),
        ('ADMIN', 'admin'),
    )
    group = models.CharField(
        max_length=10,
        choices= GROUP_CHOICES,
        default=USER
    )
    email = models.EmailField(
        unique=True,
        blank=False
    )
    username = models.CharField(
        max_length=150,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.group == self.ADMIN

    @property
    def is_moderator(self):
        return self.group == self.MODERATOR

    class Meta:
        ordering= ['id']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(
                    username__iexact='me'
                ),
                name="username_is_not_me"
            )
        ]


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']


class Tittle(models.Model):
    name = models.CharField(max_length=256, unique=True)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='tittles'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='tittles'
    )

    def save(self, *args, **kwargs):
        if self.year > datetime.date.today().year:
            raise ValidationError('Нельзя добавлять произведения, которые еще не вышли.')
        super(Tittle, self).save(*args, *kwargs)


# vovq: ожидает модели Title


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='reviews'
    # )

    class Meta:
        ordering = ['-pub_date']
        # unique_together = ('author', 'title')

    def __str__(self) -> str:
        return self.text[:10]


class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.text[:10]

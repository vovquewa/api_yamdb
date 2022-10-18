from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        ('USER', 'user'),
        ('MODERATOR', 'moderator'),
        ('ADMIN', 'admin'),
    )
    role = models.CharField(
        max_length=10,
        choices= ROLE_CHOICES,
        default=USER
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        blank=False
    )
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True
    )
    bio = models.TextField(
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

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

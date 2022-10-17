from django.contrib.auth.models import AbstractUser
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

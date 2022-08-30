from collections import namedtuple

from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES_NAME = namedtuple('ROLES_NAME', 'user admin')
ROLES = ROLES_NAME('user', 'admin')
ROLE_CHOICES = (
    ('user', ROLES.user),
    ('admin', ROLES.admin),
)


class User(AbstractUser):
    """User model."""
    email = models.EmailField(
        'email ',
        unique=True,
        max_length=250,
    )
    username = models.CharField(
        'username',
        unique=True,
        max_length=150,
    )
    first_name = models.CharField(
        'first_name',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'last_name',
        max_length=150,
        blank=True
    )
    role = models.CharField(
        'User Role',
        max_length=max(len(role) for _, role in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=ROLES.user,
    )
    password = models.CharField('Password', max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_admin(self):
        return (
            self.role == ROLES.admin
            or self.is_staff
        )

    class Meta:
        ordering = ['username']
        verbose_name = 'User(s)'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subs')

    class Meta:
        verbose_name = 'Subscription(s)'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]

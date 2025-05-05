from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Користувач з роллю
class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)

    def __str__(self):
        return self.username

    # Уникаємо конфлікту через AbstractUser, додаючи related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

# Страховий поліс
class Policy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='policies')
    coverage = models.FloatField()

    def __str__(self):
        return f"Policy #{self.id} for {self.user.username}"

# Заява на виплату
class Claim(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='claims')
    amount = models.FloatField()

    def __str__(self):
        return f"Claim #{self.id} for Policy #{self.policy.id}"

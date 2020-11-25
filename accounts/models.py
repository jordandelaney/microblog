from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(_('email'), help_text="This will be used to login.", unique=True)
    username = models.CharField(max_length=50, help_text="Required: Username. 50 characters or less.", blank=False, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=200, help_text="Required: First Name. 200 characters or less.", blank=False)
    last_name = models.CharField(max_length=200, help_text="Required: Last Name. 200 characters or less.", blank=False)
    biography = models.TextField(help_text='Tell us about yourself.', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14)
    address = models.TextField()
    student = models.BooleanField(default=False, null=True, blank=True)
    learning_place = models.CharField(max_length=150, null=True, blank=True)
    employee = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    # Define related_name attribute to avoid clashes with auth.User model
    related_name = 'custom_user_groups'

    def __str__(self):
        return self.username
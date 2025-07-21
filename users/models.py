from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT = 'ST'
    INSTRUCTOR = 'IN'
    USER_ROLE_CHOICES = {
        STUDENT: 'Student',
        INSTRUCTOR: 'Instructor',
    }
    role = models.CharField(
        max_length=2,
        choices=USER_ROLE_CHOICES,
        default=STUDENT
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
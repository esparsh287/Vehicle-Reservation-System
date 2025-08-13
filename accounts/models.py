from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  ROLE_CHOICES=[
    ('user', 'Regular User'),
    ('owner', 'Vehicle Owner')
  ]
  role=models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
  phone_number=models.CharField(max_length=10)
  address=models.CharField(max_length=100)

  def __str__(self):
    return self.username
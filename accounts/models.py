from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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
  

class Vehicle(models.Model):
  VEHICLE_TYPES = [('car', 'Car'), ('van', 'Van'), ('bus', 'Bus'), ('truck', 'Truck')]
  vehicle_name = models.CharField(max_length=100)
  vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES, default='car')
  capacity = models.PositiveIntegerField()
  vehicle_number = models.CharField(max_length=50, unique=True)
  description = models.TextField(blank=True, null=True)
  is_active = models.BooleanField(default=False)  # Active only after admin approval
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
  photo=models.ImageField(upload_to='vehicles/')

  def __str__(self):
    return f'{self.vehicle_name} | {self.vehicle_type}'
  

  

 

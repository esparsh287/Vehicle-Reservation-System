from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

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
  

class KYCForm(models.Model):
  vehicle=models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='kyc_forms')
  citizenship_number = models.CharField(max_length=50)
  license_number = models.CharField(max_length=50)
  document= models.ImageField(upload_to="kyc/")
  dob=models.DateField()
  kyc_submitted_at = models.DateTimeField(auto_now_add=True)
  kyc_approved = models.BooleanField(default=False)
  kyc_approved_at = models.DateTimeField(blank=True, null=True)


  def save(self,*args, **kwargs):
    if self.vehicle:
      if self.kyc_approved and self.kyc_approved_at is None:
        self.kyc_approved_at= timezone.now()
        self.vehicle.is_active= True
        self.vehicle.save()
      
      elif not self.kyc_approved:
        self.kyc_approved_at= None
        self.vehicle.is_active=False
        self.vehicle.save()
    
    super().save(*args, **kwargs)
    

  def __str__(self):
    return self.vehicle.vehicle_name



class Booking(models.Model):
  STATUS_CHOICES=[
    ('pending','Pending'),
    ('approved', 'Approved'),
    ('rejected','Rejected'),
    ('cancelled','Cancelled'),
  ]
  user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reservations')
  vehicle=models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reservations')
  start_date=models.DateField()
  end_date=models.DateField()
  pickup_location=models.CharField(max_length=300)
  destination=models.CharField(max_length=200)
  purpose=models.CharField(max_length=255)
  status=models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user}|{self.vehicle}|{self.start_date}"

  



 

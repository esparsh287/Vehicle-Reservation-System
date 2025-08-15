from django.contrib import admin
from .models import CustomUser, Vehicle, KYCForm

admin.site.register(CustomUser)
admin.site.register(Vehicle)
admin.site.register(KYCForm)
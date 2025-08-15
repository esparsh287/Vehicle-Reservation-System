from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('kyc_form/', views.kyc_view, name='kyc')
]


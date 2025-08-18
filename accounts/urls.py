from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('kyc_form/', views.kyc_view, name='kyc'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]


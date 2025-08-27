from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('kyc_form/', views.kyc_view, name='kyc'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('update_profile/<int:pk>/', views.update_profile, name='update_profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('admin_kyc/<str:status>/', views.admin_kyc_view, name='admin_kyc_view')
]


from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='home'),
    path('about/', views.about, name='about'),
    path('categories/<str:name>/', views.categories, name='categories'),
    path('search/', views.search, name='search'),
    path('book/<int:pk>', views.booking, name='booking'),
    path('reservations/', views.reservations, name='reservations'),
    path('cancel_reservation/<int:pk>/', views.cancel_reservation, name='cancel_reservation')
]

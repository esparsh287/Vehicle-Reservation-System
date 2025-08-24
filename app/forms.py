from django import forms
from accounts.models import Booking


class BookingForm(forms.ModelForm):
  start_date = forms.DateField(label="", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Start Date', 'type':'date'}))
  end_date = forms.DateField(label="", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'End Date', 'type':'date'}))
  pickup_location = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pickup Address'}))
  destination = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destination Address'}))
  purpose = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Purpose for reservation'}))

  class Meta:
    model=Booking
    fields=['start_date', 'end_date', 'pickup_location', 'destination', 'purpose']



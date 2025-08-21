from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from .models import Vehicle, KYCForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    phone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    
    vehicle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle Name'}))
    vehicle_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle Number'}))
    capacity = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle Capacity'}))
    description = forms.CharField(label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle Description'}))
    photo = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    vehicle_type = forms.ChoiceField(
        label='',
        choices=Vehicle.VEHICLE_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2', 'phone_number', 'address', 'vehicle_name', 'vehicle_number', 'capacity', 'description', 'photo', 'vehicle_type')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data.get('role') == 'owner':
                Vehicle.objects.create(
                    owner=user,
                    vehicle_name=self.cleaned_data.get('vehicle_name'),
                    vehicle_number=self.cleaned_data.get('vehicle_number'),
                    vehicle_type=self.cleaned_data.get('vehicle_type'),
                    capacity=self.cleaned_data.get('capacity'),
                    description=self.cleaned_data.get('description'),
                    photo=self.cleaned_data.get('photo')
                    
                )
        return user
    

class KYCform(forms.ModelForm):
    class Meta:
        model=KYCForm
        fields=['citizenship_number', 'license_number', 'dob', 'document']


class UserUpdateForm(UserChangeForm):
    class Meta:
        model=CustomUser
        fields=['username','email', 'first_name', 'last_name', 'phone_number', 'address']

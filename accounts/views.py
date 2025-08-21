from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, KYCform, UserUpdateForm
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # Save user (Vehicle will be created in form.save())
            user = form.save()
            messages.success(request, "Account created successfully!")
            login(request, user)

            if form.cleaned_data['role'] == 'owner':
                # Redirect owners to KYC form
                return redirect('kyc')

            # Login regular users
            login(request, user)
            return redirect('login')  # Replace with your actual home page URL

        else:
            messages.error(request, "Error occurred during registration!")
    else:
        form = SignUpForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['password']
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Sucessful!!!!")
            return redirect('home')
        else:
            messages.error(request, "Error During Login")
            return redirect('login')
    return render(request, 'accounts/login.html',{})


def logout_view(request):
    logout(request)
    messages.success(request, "You have Logged out.... Thanks for stopping by!!!")
    return redirect('login')


def kyc_view(request):
    if request.method == "POST":
        form = KYCform(request.POST, request.FILES)
        if form.is_valid():
            kyc = form.save(commit=False)
            vehicle = request.user.vehicles.first()  # Get the vehicle created at registration
            if not vehicle:
                messages.error(request, "No vehicle found for this user!")
                return redirect('kyc')
            kyc.vehicle = vehicle
            kyc.save()
            messages.success(request, "KYC submitted successfully")
            return render(request, 'accounts/kyc_wait.html')
        else:
            messages.error(request, "Something went wrong!!!")
            return redirect('kyc')
    else:
        form = KYCform()
    return render(request, 'accounts/kyc_form.html', {'form': form})


@login_required
def profile(request, pk):
    user=CustomUser.objects.get(pk=pk)
    return render(request, 'accounts/profile.html',{'user':user})


def update_profile(request, pk):
    user= CustomUser.objects.get(pk=pk)
    if request.method=="POST":
        form=UserUpdateForm(request.POST, instance= user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Update Sucessfully!!!")
            return redirect('profile', user.id)
        else:
            messages.error(request, "Profile Update Failed")
            return redirect('home')
    
    return render(request, 'accounts/update_profile.html', {'user':user})

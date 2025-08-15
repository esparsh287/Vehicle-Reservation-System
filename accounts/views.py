from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, KYCform
from django.contrib import messages

# Registration view
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
            return redirect('home')  # Replace with your actual home page URL

        else:
            messages.error(request, "Error occurred during registration!")
    else:
        form = SignUpForm()

    return render(request, 'accounts/register.html', {'form': form})


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

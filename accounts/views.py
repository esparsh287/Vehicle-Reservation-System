from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, KYCform, UserUpdateForm, UserPasswordForm
from django.contrib import messages
from .models import CustomUser, KYCForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now



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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log in first

            if user.role == "owner":
                kycs = KYCForm.objects.filter(vehicle__in=user.vehicles.all())
                if not kycs.exists():
                    messages.warning(request, "You must submit your KYC before proceeding.")
                    return redirect('kyc')

                # If none of the KYCs are approved, show wait page
                approved = kycs.filter(kyc_approved=True).exists()
                if not approved:
                    messages.warning(request, "Your KYC is pending approval. Please wait.")
                    return render(request, 'accounts/kyc_wait.html')

            # Owner with approved KYC OR regular customer → allow home access
            messages.success(request, "Login successful!")
            return redirect('home')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'accounts/login.html', {})





def logout_view(request):
    logout(request)
    messages.success(request, "You have Logged out.... Thanks for stopping by!!!")
    return redirect('login')


def kyc_view(request):
    if request.method == "POST":
        form = KYCform(request.POST, request.FILES)
        if form.is_valid():
            kyc = form.save(commit=False)
            vehicle = request.user.vehicles.first()
            if not vehicle:
                messages.error(request, "No vehicle found for this user!")
                return redirect('kyc')

            kyc.vehicle = vehicle
            kyc.save()
            messages.success(request, "KYC submitted successfully, please wait for approval")
            return render(request, 'accounts/kyc_wait.html')

        else:
            messages.error(request, "Something went wrong!!!")
            return redirect('kyc')

    else:
        existing_kyc = KYCForm.objects.filter(vehicle__in=request.user.vehicles.all()).first()
        if existing_kyc:
            # Always show wait page after submission until admin approves
            return render(request, 'accounts/kyc_wait.html')

        form = KYCform()
    return render(request, 'accounts/kyc_form.html', {'form': form})



@login_required
def profile(request, pk):
    user=CustomUser.objects.get(pk=pk)
    return render(request, 'accounts/profile.html',{'user':user})


@login_required
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

@login_required
def update_password(request):
    if request.method=="POST":
        form= UserPasswordForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            messages.success(request, "Password Changed Sucessfully!!!")
            return redirect('login')
        else:
            messages.error(request,"Error")
    else:
        form= UserPasswordForm(request.user)
    return render(request, 'accounts/update_password.html',{'form': form})



def admin_kyc_view(request, status):
    if request.method == "POST" and status == "approved":
        kyc_id = request.POST.get("kyc_id")
        try:
            kyc = KYCForm.objects.get(id=kyc_id)
            kyc.kyc_approved = True
            kyc.kyc_approved_at = now()
            kyc.save()
            messages.success(request, "KYC Approved successfully ✅")
        except KYCForm.DoesNotExist:
            messages.error(request, "KYC not found ❌")
        return redirect("admin_kyc_view", status="pending")  # after approval go back to pending list

    elif status == "approved":
        kycs = KYCForm.objects.filter(kyc_approved=True)
        return render(request, "accounts/kyc_approved.html", {"kycs": kycs})

    elif status == "pending":
        kycs = KYCForm.objects.filter(kyc_approved=False)
        return render(request, "accounts/kyc_pending.html", {"kycs": kycs})

    else:
        messages.error(request, "Invalid Status!!!")
        return redirect("home")


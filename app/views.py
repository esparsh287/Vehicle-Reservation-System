from django.shortcuts import render


#@login_required
def dashboard(request):
    if hasattr(request.user, 'vehicles'):
        pending_vehicles = request.user.vehicles.filter(is_active=False)
        if pending_vehicles.exists():
            return render(request, 'accounts/kyc_wait.html')

    return render(request, 'app/dashboard.html') 
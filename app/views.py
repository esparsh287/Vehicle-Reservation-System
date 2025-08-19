from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Vehicle


@login_required
def dashboard(request):
    if hasattr(request.user, 'vehicles'):
        pending_vehicles = request.user.vehicles.filter(is_active=False)
        if pending_vehicles.exists():
            return render(request, 'accounts/kyc_wait.html')
    
    veheicles=Vehicle.objects.all()
    return render(request, 'app/dashboard.html', {'vehicles':veheicles}) 


def about(request):
    return render(request, 'app/about.html',{})

def categories(request, name):
    vehicles=Vehicle.objects.filter(vehicle_type=name.lower())
    if name == 'car':
        return render(request, 'app/car.html',{'vehicles': vehicles})
    elif name == 'van':
        return render(request, 'app/van.html',{'vehicles': vehicles})
    elif name == 'bus':
        return render(request, 'app/bus.html',{'vehicles': vehicles})
    else:
        return render(request, 'app/truck.html',{'vehicles': vehicles})
    
    
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
    return render(request, 'app/vechicle.html',{'vehicles': vehicles, 'name':name})
   
    

def search(request):
    if request.method=="POST":
        result= request.POST['search']
        vechicles= Vehicle.objects.filter(vehicle_name__icontains= result)
        return render(request, 'app/search.html', {'vehicles': vechicles})
    return render(request, 'app/search.html', {})
    
    
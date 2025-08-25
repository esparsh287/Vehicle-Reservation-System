from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Vehicle, Booking
from .forms import BookingForm
from django.contrib import messages


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



def booking(request, pk):
    vehicle= Vehicle.objects.get(pk=pk)
    if request.method=="POST":
        form=BookingForm(request.POST)
        if form.is_valid():
            active_booking= Booking.objects.filter(user=request.user).exclude(status__in=['cancelled', 'rejected', 'completed'])
            if active_booking:
                messages.error(request, "You already ahve an active reservation. Please cancel it to make another one.")
                return redirect('reservations')
            booking=form.save(commit=False)
            booking.user= request.user
            booking.vehicle=vehicle
            booking.save()
            messages.success(request, "Booking Sucessfull!!!")
            return redirect('home')
    form= BookingForm()
    print(vehicle)
    return render(request, 'app/booking.html', {'vehicle':vehicle, 'form': form})


def reservations(request):
    obj= Booking.objects.filter(user= request.user).first()
    return render(request, 'app/reservations.html', {'obj':obj})



def cancel_reservation(request, pk):
    if request.method=="POST":
        reservation= Booking.objects.get(pk=pk, user= request.user)
        reservation.delete()
        messages.success(request, "Your ride has been cancelled!!!")
        return redirect('home')
    return redirect('reservations')

    

    
    
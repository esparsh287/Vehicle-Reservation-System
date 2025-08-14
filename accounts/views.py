from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from .forms import SignUpForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Vehicle

def register(request):
  if request.method=="POST":
    form=SignUpForm(request.POST, request.FILES)
    if form.is_valid():
      user=form.save()
      messages.success(request, "Account created successfully!!!")
      login(request,user)
      return HttpResponse('<h1>Home Page</h1>')
    else:
      messages.error(request, 'Error Occurred')
      return HttpResponse('<h1>Error</h1>')
  else:
    form=SignUpForm()
    
  return render(request, 'accounts/register.html', {'form':form})



 
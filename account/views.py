from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db import IntegrityError

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')


def logout_url(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    try: 
        profile = UserInfo.objects.get(user_id=request.user.id)
    except UserInfo.DoesNotExist:
        profile = ''
    

    if request.method == 'POST':
        image = request.FILES['pro-image']
        try:
            UserInfo.objects.create(
                user=request.user,
                profile=image
            )
            return redirect('profile')
        except IntegrityError:
            user = UserInfo.objects.get(user_id=request.user.id)
            user.profile = image
            user.save()
            return redirect('profile')


    data = {
        'profile' : profile
    }
    return render(request, 'profile.html', data)


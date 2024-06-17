from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages

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
            if request.POST.get('next'):
                url = request.POST.get('next')
            else:
                url = reverse('dashboard')  
            return redirect(url)
        else:
            messages.error(request, 'Wrong Mobile or Password')
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


def update_day_status(request):
    day = request.POST['day']
    get_day = UserInfo.objects.get(user_id=request.user.id)

    if day == 'true':
        get_day.day = True
        get_day.save()
    else:
        get_day.day = False
        get_day.save()

    return JsonResponse({'success':True})

def update_night_status(request):
    night = request.POST['day']
    get_night = UserInfo.objects.get(user_id=request.user.id)

    if night == 'true':
        get_night.night = True
        get_night.save()
    else:
        get_night.night = False
        get_night.save()

    return JsonResponse({'success':True})
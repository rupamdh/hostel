from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.contrib import messages

# Create your views here.

def add_mill(request):
    users = User.objects.all().exclude(is_superuser=True)
    if request.method == 'POST':
        date = request.POST['date']
        mills_to_add = []
        for user in users:
            mill = request.POST.get(f'mill_{user.id}')
            g_mill = request.POST.get(f'g_mill{user.id}')
            mills_to_add.append(Mill(date=date, user=user, mill=mill, g_mill=g_mill))
        
        try:
            with transaction.atomic():
                Mill.objects.bulk_create(mills_to_add)
                messages.success(request, 'Mills added successfully.')
        except IntegrityError:
            messages.error(request, 'Mill already exists for this date and user.')

 
    context = {
        'users': users,
    }
    return render(request, 'mill-add.html', context)
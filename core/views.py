from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
from django.db.models import Sum

c_m = datetime.now().month
c_y = datetime.now().year


# Create your views here.
def home_page(request):
    return render(request, 'index.html')



@login_required
def dashboard(request):
    bazars = Bazar.objects.filter(date__month=c_m, user_id=request.user.id)
    total_bazar = bazars.aggregate(Sum('amount'))['amount__sum'] if bazars else 0
    mills = Mill.objects.filter(user_id=request.user.id)
    total_mill = mills.aggregate(Sum('mill_count'))['mill_count__sum'] if mills else 0


    data = {
        'total_bazar' : total_bazar,
        'total_mill' : total_mill
    }
    return render(request, 'dashboard.html', data)


@login_required
def bazar_add(request):
    users = User.objects.all().exclude(is_superuser=True).order_by('id')
    bazars = Bazar.objects.filter(date__month=c_m, date__lt=datetime.now(), user_id=request.user.id, amount=0)

    dates = []
    for bazar in bazars:
        dates.append(bazar.date.strftime("%Y-%m-%d"))
    bazar_date = dates[0] if len(dates) != 0 else ''

    if request.method == 'POST':
        date = request.POST['date']
        total_mill = 0
        for user in users:
            mill = int(request.POST.get(f'm-{user.id}'))
            get_user = User.objects.get(id=user.id)
            total_mill += mill
            Mill.objects.create(
                date=date,
                user=get_user,
                mill_count=mill
            )
        bazar = Bazar.objects.get(date=bazar_date)
        bazar.amount = (total_mill*10)+20
        bazar.save()

        return redirect('bazar-list')

    data = {
        'users' : users,
        'bazars' : bazars,
        'bazar_date' : bazar_date
    }
    return render(request, 'bazar-add.html', data)


@login_required
def bazar_list(request):
    bazars = Bazar.objects.filter(date__month=c_m, user_id=request.user.id).exclude(amount=0).order_by('-date')
    total_bazar = bazars.aggregate(Sum('amount'))['amount__sum'] if bazars else 0
    bookings = Bazar.objects.filter(date__month=c_m, user_id=request.user.id).exclude(amount__gt=0).order_by('date')
    print(bookings)


    data = {
        'bazars' : bazars,
        'total_bazar' : total_bazar,
        'bookings' : bookings
    }
    return render(request, 'bazar-list.html', data)


@login_required
def bazar_book(request):
    bazars = Bazar.objects.filter(date__month=c_m).exclude(amount=0)
    bookings = Bazar.objects.filter(date__month=c_m, amount=0)

    if request.method == 'POST':
        date = request.POST['date']
        Bazar.objects.create(
            date=date,
            user=request.user,
            amount=0
        )
        


    data = {
        'bazars' : bazars,
        'bookings' : bookings
    }
    return render(request, 'bazar-book.html', data)


@login_required
def delete_booking(request, id):
    booking = Bazar.objects.get(id=id)
    booking.delete()

    return redirect('bazar-list')

@login_required
def delete_bazar(request, id):
    bazar = Bazar.objects.get(id=id)
    mills = Mill.objects.filter(date=bazar.date)
    mills.delete()
    bazar.amount = 0
    bazar.save()

    return redirect('bazar-list')


@login_required
def bazar_edit(request, id):
    bazar = Bazar.objects.get(id=id)
    date = bazar.date
    get_date = date.strftime("%Y-%m-%d")
    mills = Mill.objects.filter(date=date)

    total_mill = 0
    if request.method == 'POST':
        for mill in mills:
            mill_count = int(request.POST.get(f'm-{mill.id}'))
            get_mill = Mill.objects.get(id=mill.id)
            get_mill.mill_count = mill_count
            get_mill.save()
            total_mill += mill_count
        bazar.amount = (total_mill*10)+20
        bazar.save()
        return redirect('bazar-list')
    


    data = {
        'get_date' : get_date,
        'mills' : mills
    }
    return render(request, 'bazar-edit.html', data)

@login_required
def mill_list(request):
    return render(request, 'mill.html')
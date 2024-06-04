from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from datetime import datetime, timedelta
from django.db.models import Sum
from account.models import *


c_m = datetime.now().month
c_y = datetime.now().year


# Create your views here.
def home_page(request):
    



    return render(request, 'index.html')

@login_required
def dashboard(request):
    bazars = Bazar.objects.filter(date__month=c_m, user_id=request.user.id)
    total_bazar = bazars.aggregate(Sum('amount'))['amount__sum'] if bazars else 0
    mills = Mill.objects.filter(user_id=request.user.id, date__month=c_m)
    total_mill = mills.aggregate(Sum('mill_count'))['mill_count__sum'] if mills else 0
    exps = Establish.objects.filter(date__month=c_m, user_id=request.user.id)
    total_exp = exps.aggregate(Sum('amount'))['amount__sum'] if exps else 0
    total_diposit = total_bazar+total_exp

    upc_bazar = Bazar.objects.filter(date__month=c_m, date__gt=datetime.now(), user_id=request.user.id, amount=0)
    try:
        today_bazar = Bazar.objects.get(date=datetime.today())
    except Bazar.DoesNotExist:
        today_bazar = ''
    tmr_bazar = Bazar.objects.filter(date__month=c_m, date__day=datetime.now().day+1)
    
    userinfo = UserInfo.objects.get(user_id=request.user.id)

    try:
        bill = Bill.objects.get(date__month=datetime.now().month-1, user=request.user)
    except Bill.DoesNotExist:
        bill = ''
    


    data = {
        'total_diposit' : total_diposit,
        'total_mill' : total_mill,
        'upc_bazar' : upc_bazar,
        'today_bazar' : today_bazar,
        'tmr_bazar' : tmr_bazar,
        'day' : userinfo.day,
        'night' : userinfo.night,
        'bill' : bill
    }
    return render(request, 'dashboard.html', data)


@login_required
def quick_book(request):
    try:
        Bazar.objects.create(
            date=datetime.today() + timedelta(days=1),
            user=request.user,
            amount=0
        )
        return redirect('dashboard')
    except:
        return redirect('dashboard')
    



@login_required
def bazar_add(request):
    users = User.objects.all().exclude(is_superuser=True).order_by('id')
    bazars = Bazar.objects.filter(date__lte=datetime.now(), user_id=request.user.id, amount=0).order_by('date')

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
    bookings = Bazar.objects.filter(date__month=c_m, date__gt=datetime.today(), user_id=request.user.id).exclude(amount__gt=0).order_by('date')


    data = {
        'bazars' : bazars,
        'total_bazar' : total_bazar,
        'bookings' : bookings
    }
    return render(request, 'bazar-list.html', data)


@login_required
def bazar_book(request):
    bazars = Bazar.objects.all().exclude(amount=0)
    bookings = Bazar.objects.filter(amount=0)
    

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
    mills = Mill.objects.filter(date__month=c_m, user_id=request.user.id)
    total_mill = mills.aggregate(Sum('mill_count'))['mill_count__sum']
    
    data = {
        'mills' : mills,
        'total_mill' : total_mill
    }
    return render(request, 'mill.html', data)

@login_required
def add_est(request):
    if request.method == 'POST':
        Establish.objects.create(
            date=request.POST['date'],
            user=request.user,
            reasone=request.POST['reasone'],
            amount=request.POST['amount']
        )
    return render(request, 'est-add.html')

@login_required
def est_list(request):
    exps = Establish.objects.filter(date__month=c_m, user_id=request.user.id)

    data = {
        'exps' : exps
    }
    return render(request, 'est-list.html', data)

@login_required
def est_edit(request, id):
    exp = Establish.objects.get(id=id)
    if request.method == 'POST':
        exp.date = request.POST['date']
        exp.reasone = request.POST['reasone']
        exp.amount = request.POST['amount']
        exp.save()
        return redirect('est-list')

    data = {
        'exp' : exp
    }
    return render(request, 'est-edit.html', data)

@login_required
def est_delete(request, id):
    exp = Establish.objects.get(id=id)
    exp.delete()

    return redirect('est-list')


@login_required
def get_bill(request):
    users = User.objects.all().exclude(is_superuser=True)
    total_mill = 0
    for user in users:
        mills = Mill.objects.filter(date__month=p_m, user=user)
        mill = mills.aggregate(Sum('mill_count'))['mill_count__sum'] if mills else 0
        total_mill += mill
    print(total_mill)


    data = {
        'users' : users
    }
    return render(request, 'bill.html', data)











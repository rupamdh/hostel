from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from datetime import datetime
from django.db.models import Sum

# Create your models here.
class Mill(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mill_count = models.IntegerField()

    def __str__(self):
        return f'{self.date} - {self.user.first_name} - {self.mill_count}'
    

class Bazar(models.Model):
    date = models.DateField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.date} - {self.user.first_name} - {self.amount}'


class Establish(models.Model):
    EST_CHOICES = (
        ("GG", "Ginger & Garlic"),
        ("OI", "Oil"),
        ("CH", "Green Chilli"),
        ("GS", "Gas"),
        ("OT", "Other"),
    )

    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reasone = models.CharField(max_length=2, choices=EST_CHOICES)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.date} - {self.user.first_name} - {self.amount}'

class Bill(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mill = models.IntegerField(default=0)
    mill_cost = models.FloatField(default=0)
    establish = models.FloatField(default=0)
    total_cost = models.IntegerField(default=0)
    diposit = models.IntegerField(default=0)
    due = models.IntegerField(default=0)

    class Meta:
        unique_together = (('date', 'user'),)

    def __str__(self):
        return f'{self.date} - {self.user.first_name}'

p_m = datetime.now().month - 1

class Others(models.Model):
    date = models.DateField(unique=True)
    electric = models.IntegerField()
    cook = models.IntegerField()
    rice = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        #with transaction.atomic():        
        users = User.objects.all().exclude(is_superuser=True)
        total_user = users.count()

        for user in users:
            try:
                bill, created = Bill.objects.get_or_create(date=self.date, user=user)
                my_mill = Mill.objects.filter(date__month=p_m, user=user).aggregate(Sum('mill_count'))['mill_count__sum']
                total_mill = Mill.objects.filter(date__month=p_m).aggregate(Sum('mill_count'))['mill_count__sum']
                total_bazar = Bazar.objects.filter(date__month=p_m).aggregate(Sum('amount'))['amount__sum']
                mill_charge = (total_bazar+self.rice)/total_mill
                establish = Establish.objects.filter(date__month=p_m).aggregate(Sum('amount'))['amount__sum'] if Establish.objects.filter(date__month=p_m) else 0
                my_bazar = Bazar.objects.filter(date__month=p_m, user=user).aggregate(Sum('amount'))['amount__sum'] if Bazar.objects.filter(date__month=p_m, user=user) else 0
                my_establish = Establish.objects.filter(date__month=p_m, user=user).aggregate(Sum('amount'))['amount__sum'] if Establish.objects.filter(date__month=p_m, user=user) else 0

                #if created:
                bill.mill = my_mill
                bill.mill_cost = my_mill*mill_charge
                bill.establish = (establish+self.cook+self.electric)/total_user
                bill.total_cost = round(bill.mill_cost + bill.establish)
                bill.diposit = my_establish+my_bazar
                bill.due = round(bill.total_cost - bill.diposit)
                print(bill.due)
                bill.save()
            except IntegrityError:
                print('Error')
                pass
            


    def __str__(self):
        return f'{self.date}'
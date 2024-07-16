from django.db import models
from datetime import datetime

last_month = datetime.now().month - 1

class MillQuerySet(models.QuerySet):
    def this_month(self):
        return self.filter(date__month=datetime.now().month)
    
    def last_month(self):
        return self.filter(date__month=last_month)
    
    def my_this_month(self, user):
        return self.filter(date__month=datetime.now().month, user=user)
    
    def my_last_month(self, user):
        return self.filter(date__month=last_month, user=user)
    
class MillManager(models.Manager):
    def get_queryset(self):
        return MillQuerySet(self.model, using=self._db)
    
    def this_month(self):
        return self.get_queryset().this_month()
    
    def last_month(self):
        return self.get_queryset().last_month()
    
    def total_this_month(self):
        return self.this_month().aggregate(total=models.Sum('mill'))['total']
    
    def total_last_month(self):
        return self.last_month().aggregate(total=models.Sum('mill'))['total']
    
    def my_this_month(self, user):
        return self.get_queryset().my_this_month(user)
    
    def my_last_month(self, user):
        return self.get_queryset().my_last_month(user)
    
    def total_my_this_month(self, user):
        return self.my_this_month(user).aggregate(total=models.Sum('mill'))['total']
    
    def total_my_last_month(self, user):
        return self.my_last_month(user).aggregate(total=models.Sum('mill'))['total']
    

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mill(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mill_count = models.IntegerField()

    def __str__(self):
        return f'{self.date} - {self.user} - {self.mill_count}'
    

class Bazar(models.Model):
    date = models.DateField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.date} - {self.user} - {self.amount}'

class Booking(models.Model):
    date = models.DateField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} - {self.user}'


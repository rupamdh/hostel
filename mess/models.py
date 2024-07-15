from django.db import models
from django.contrib.auth.models import User
#import user model from django 

# Create your models here.
class Mill(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mill = models.IntegerField()
    g_mill = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.user.first_name} - {self.mill}"
    
    class Meta:
        verbose_name_plural = "Mills"
        unique_together = ('date', 'user',)

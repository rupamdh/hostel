from django.contrib.auth.models import BaseUserManager
from django.db import models

class UserQuerySet(models.QuerySet):
    def active_users(self):
        return self.filter(is_active=True)
    


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number must be provided")
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)
    
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)
    
    def active_users(self):
        return self.get_queryset().active_users()
    
    
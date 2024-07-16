from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager



class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=12, unique=True)
    profile_image = models.ImageField(upload_to='user/', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Ensure password is hashed when saving user
        if self.pk is None:  # New user (not updating existing)
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone
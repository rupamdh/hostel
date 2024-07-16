from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_dashboard, name='admin-dashboard'),
]

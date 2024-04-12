"""
URL configuration for mess project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *
from account.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('login/', login_page, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_url, name='logout'),

    path('bazar-add/', bazar_add, name='bazar-add'),
    path('bazar-list/', bazar_list, name='bazar-list'),
    path('bazar-book/', bazar_book, name='bazar-book'),
    path('delete-bazar/<int:id>/', delete_bazar, name='delete-bazar'),
    path('edit-bazar/<int:id>/', bazar_edit, name='bazar-edit'),
    path('delete-booking/<int:id>/', delete_booking, name='delete-booking'),

    path('mill/', mill_list, name='mill'),
]

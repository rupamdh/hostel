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

from django.conf import settings
from django.conf.urls.static import static
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
    path('quick-book/', quick_book, name='quick-book'),

    path('bazar-add/', bazar_add, name='bazar-add'),
    path('bazar-list/', bazar_list, name='bazar-list'),
    path('bazar-book/', bazar_book, name='bazar-book'),
    path('delete-bazar/<int:id>/', delete_bazar, name='delete-bazar'),
    path('edit-bazar/<int:id>/', bazar_edit, name='bazar-edit'),
    path('delete-booking/<int:id>/', delete_booking, name='delete-booking'),

    path('add-establish/', add_est, name='add-est'),
    path('est-list/', est_list, name='est-list'),
    path('edit-est/<int:id>/', est_edit, name='edit-est'),
    path('delete-est/<int:id>/', est_delete, name='delete-est'),

    path('mill/', mill_list, name='mill'),
    path('chday/', update_day_status, name='chday'),
    path('chnight/', update_night_status, name='chnight'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
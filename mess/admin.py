from django.contrib import admin
from django.http import HttpRequest
from django.template.response import TemplateResponse
from .models import *
# Register your models here.

class MillAdmin(admin.ModelAdmin):
    #change_form_template = 'admin/mess/mill/change_form.html'  # Path to your custom template
    def changelist_view(self, request, extra_context=None):
        self.change_list_template = 'admin/mess/mill/change_list.html'
        extra_context = extra_context or {}
        extra_context['title'] = 'Mess Mill'
        extra_context['users'] = User.objects.all().exclude(is_superuser=True)
        

        return super().changelist_view(request, extra_context)

admin.site.register(Mill, MillAdmin)
from django import template
from account.models import *
from datetime import datetime

register = template.Library()

@register.filter
def get_profile_image(id):
    try:
        user = UserInfo.objects.get(user_id=id)
        return user.profile
    except UserInfo.DoesNotExist:
        return '/profile/user.jpg'    
    
@register.tag
def get_due_date():
    return datetime.now().year
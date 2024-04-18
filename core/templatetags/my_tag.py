from django import template
from account.models import *

register = template.Library()

@register.filter
def get_profile_image(id):
    try:
        user = UserInfo.objects.get(user_id=id)
        return user.profile
    except UserInfo.DoesNotExist:
        return '/profile/user.jpg'    
    
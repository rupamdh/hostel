from django import template
from account.models import User

register = template.Library()

@register.simple_tag
def get_users():
    users = User.objects.active_users()
    return users


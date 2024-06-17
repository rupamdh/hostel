from django import template
from account.models import *
from datetime import datetime, timedelta
from core.models import *
register = template.Library()

@register.filter
def get_profile_image(id):
    try:
        user = UserInfo.objects.get(user_id=id)
        return user.profile
    except UserInfo.DoesNotExist:
        return '/profile/user.jpg'
    
def get_day_after_5_days(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    new_date = date_obj + timedelta(days=5)
    return new_date.strftime('%B %d, %Y')



@register.filter(name='due_date')
def get_due_date(id):
    bill = Bill.objects.get(id=id)
    date = f'{bill.date.year}-{bill.date.month}-{bill.date.day}'

    due_date = get_day_after_5_days(date)

    return due_date


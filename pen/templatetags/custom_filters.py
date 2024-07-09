from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_item(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None

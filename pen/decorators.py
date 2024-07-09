from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def user_is_staff(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/error-page/?message=Master%20only%20can%20access%20this%20page',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def user_is_not_staff(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_staff,
        login_url='/error-page/?message=Writer%20only%20can%20access%20this%20page',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def user_is_superuser(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/error-page/?message=Admin%20only%20can%20access%20this%20page',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

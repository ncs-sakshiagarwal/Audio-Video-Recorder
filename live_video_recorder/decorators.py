from django.contrib.auth.decorators import user_passes_test
from .models import Role, UserProfile

def role_required(*role_names):
    def decorator(view_func):
        @user_passes_test(lambda u: u.userprofile.role.name in role_names)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

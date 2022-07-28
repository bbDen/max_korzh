from django.contrib import admin as contrib_admin
from django.contrib.auth import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@contrib_admin.register(User)
class UserAdmin(admin.UserAdmin):
    list_display = ['username']
    fieldsets = (
        (
            "Fields",
            {
                "fields": (
                    "email",
                    "last_login",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "password",
                )
            },
        ),
    )


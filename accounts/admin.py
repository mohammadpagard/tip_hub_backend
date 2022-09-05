# Django packages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Local apps
from .models import User, OtpCode
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'email', 'fullname', 'is_admin')
    list_filter = ('is_active', 'is_admin')

    fieldsets = (
        ('Main', {'fields': (
            'email', 'phone_number', 'fullname', 'bio', 'age', 'image', 'password'
        )}),
        ('Permissions', {'fields': (
            'is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}
         ),
    )

    add_fieldsets = (
        (None, {'fields': (
            'phone_number', 'email', 'fullname', 'password1', 'password2')}
         ),
    )

    search_fields = ('phone_number', 'email', 'fullname')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disable = True
        return form


admin.site.register(User, UserAdmin)
admin.site.register(OtpCode)

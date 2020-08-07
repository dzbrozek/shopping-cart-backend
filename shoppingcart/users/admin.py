from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name']
    search_fields = ['id', 'email', 'first_name', 'last_name']
    readonly_fields = ['password']


admin.site.unregister(Group)

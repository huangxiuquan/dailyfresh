from django.contrib import admin
from users.models import User, Address


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'create_time', 'last_login']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'receiver_name', 'receiver_mobile', 'detail_addr', 'zip_code']


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)

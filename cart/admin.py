from django.contrib import admin
from cart.models import CartInfo


# Register your models here.

class CartInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'count']


admin.site.register(CartInfo, CartInfoAdmin)

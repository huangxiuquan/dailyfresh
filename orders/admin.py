from django.contrib import admin
from orders.models import OrderGoods, OrderInfo


# Register your models here.

class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = []


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = []


admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)

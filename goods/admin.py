from django.contrib import admin
from goods.models import Goods, GoodsCategory, GoodsImage, IndexGoodsBanner, IndexCategoryGoodsBanner


# Register your models here.

class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'unit', 'price', 'stock', 'sales', 'status']


class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'logo']


class GoodsImageAdmin(admin.ModelAdmin):
    list_display = []


class IndexGoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku', 'image', 'index']


class IndexCategoryGoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku', 'display_type', 'index']


admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(GoodsImage, GoodsImageAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexCategoryGoodsBanner, IndexCategoryGoodsBannerAdmin)

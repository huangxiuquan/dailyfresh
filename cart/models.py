from django.db import models


# Create your models here.
class CartInfo(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)  # 买的数量

    class Meta:
        verbose_name = '购物车商品信息'
        verbose_name_plural = '购物车商品信息'

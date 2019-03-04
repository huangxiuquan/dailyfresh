from django.db import models
from utils.models import BaseModel
from tinymce.models import HTMLField


class GoodsCategory(BaseModel):
    """商品类别表"""
    name = models.CharField(max_length=20, verbose_name="名称")
    logo = models.CharField(max_length=100, verbose_name="标识")
    image = models.ImageField(upload_to="category", verbose_name="图片")

    class Meta:
        db_table = "df_goods_category"
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 返回4条分类商品用于首页展示
    def goodslist(self):
        return self.goods_set.filter(status=True)[:4]


class Goods(BaseModel):
    """商品表"""

    category = models.ForeignKey(GoodsCategory, verbose_name="类别", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="名称")
    desc = HTMLField(verbose_name="详细介绍", default="", blank=True)
    unit = models.CharField(max_length=10, verbose_name="销售单位")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.IntegerField(default=0, verbose_name="库存")
    sales = models.IntegerField(default=0, verbose_name="销量")
    default_image = models.ImageField(upload_to="goods", verbose_name="图片")
    status = models.BooleanField(default=True, verbose_name="是否上线")

    class Meta:
        db_table = "df_goods"
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):
    """商品图片"""
    sku = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="goods", verbose_name="图片")

    class Meta:
        db_table = "df_goods_image"
        verbose_name = "商品图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.sku)


class IndexGoodsBanner(BaseModel):
    """首页轮播商品展示"""
    sku = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="banner", verbose_name="图片")
    index = models.SmallIntegerField(default=0, verbose_name="顺序")

    class Meta:
        db_table = "df_index_goods"
        verbose_name = "主页轮播商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.sku)


class IndexCategoryGoodsBanner(BaseModel):
    """主页分类商品展示"""
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )
    category = models.ForeignKey(GoodsCategory, verbose_name="商品类别", on_delete=models.CASCADE)
    sku = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    display_type = models.SmallIntegerField(choices=DISPLAY_TYPE_CHOICES, verbose_name="显示类型")
    index = models.SmallIntegerField(default=0, verbose_name="顺序")

    class Meta:
        db_table = "df_index_category_goods"
        verbose_name = "主页分类展示商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.sku)


class IndexPromotionBanner(BaseModel):
    """主页促销活动展示"""
    name = models.CharField(max_length=50, verbose_name="活动名称")
    url = models.URLField(verbose_name="活动两件")
    image = models.ImageField(upload_to="active", verbose_name="图片")
    index = models.SmallIntegerField(default=0, verbose_name="顺序")

    class Meta:
        db_table = "df_index_promotion"
        verbose_name = "主页促销活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

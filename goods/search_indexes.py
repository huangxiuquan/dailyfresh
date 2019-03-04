from haystack import indexes
# 引入你项目下的model（也就是你要将其作为检索关键词的models）
from goods.models import Goods


# model名 + Index作为类名
class GoodsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # 对商品名称进行搜索
    name = indexes.CharField(model_attr='name')
    default_image = indexes.CharField(model_attr='default_image')
    price = indexes.CharField(model_attr='price')
    unit = indexes.CharField(model_attr='unit')
    id = indexes.CharField(model_attr='id')

    def get_model(self):
        return Goods

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

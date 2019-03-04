from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from haystack.views import SearchView
from dailyfresh.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE
from django.http import HttpResponse


# Create your views here.


# 定义首页
def index(request):
    # 商品大分类
    category = GoodsCategory.objects.all()
    # 轮播图
    banner = IndexGoodsBanner.objects.all()
    # 活动
    active = IndexPromotionBanner.objects.all()

    return render(request, 'goods/index.html', {'category': category, 'banner': banner, 'active': active})


# 根据分类id查看更多商品
def list(request, cid, pindex, sort):
    typeinfo = GoodsCategory.objects.get(id=cid)
    news = typeinfo.goods_set.order_by('-id')[0:2]  # 取该类型最新的两个
    # 分类下所有商品
    goods_list = Goods.objects.filter(category=cid)
    if sort == '1':  # 默认最新
        goods_list = goods_list.order_by('-id')
    elif sort == '2':  # 按价格排序
        goods_list = goods_list.order_by('price')
    elif sort == '3':  # 销量
        goods_list = goods_list.order_by('sales')

    paginator = Paginator(goods_list, 10)  # 分页, 每页有几个元素
    page = paginator.page(int(pindex))  # 获得pindex页的元素列表

    context = {
        # 'title': typeinfo.ttitle,  # 类型名称  为了给base传递title
        'page': page,  # 排序后的每页的元素列表
        'typeinfo': typeinfo,  # 类型信息
        'news': news,  # 新品推荐列表
        'sort': sort,  # 传递排序数字, 方便图标active
        'paginator': paginator,  # 分页
    }
    return render(request, 'goods/list.html', context)


# 商品详情
def detail(request, gid):
    good = Goods.objects.get(id=gid)
    typeinfo = GoodsCategory.objects.get(id=good.category_id)  # 分类
    news = typeinfo.goods_set.order_by('-id')[0:2]  # 取该类型最新的两个
    context = {
        'good': good,
        'news': news
    }
    return render(request, 'goods/detail.html', context)


# 定义搜索视图
class MySearchView(SearchView):
    def build_page(self):
        # 分页重写
        context = super(MySearchView, self).extra_context()  # 继承自带的context
        try:
            page_no = int(self.request.GET.get('page', 1))
        except Exception:
            return HttpResponse("Not a valid number for page.")

        if page_no < 1:
            return HttpResponse("Pages should be 1 or greater.")
        a = []
        for i in self.results:
            a.append(i.object)
        paginator = Paginator(a, HAYSTACK_SEARCH_RESULTS_PER_PAGE)
        page = paginator.page(page_no)
        return (paginator, page)

    def extra_context(self):
        context = super(MySearchView, self).extra_context()  # 继承自带的context
        context['title'] = '搜索'
        return context

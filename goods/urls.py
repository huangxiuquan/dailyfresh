from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:gid>/', views.detail),  # 商品详情
    path('list/<int:cid>/<int:pindex>/<int:sort>/', views.list),  # 分类id--页码--排序
    path('search/', MySearchView()),
]

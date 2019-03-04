from django.urls import path
from . import views
from cart.views import PlaceOrderView

urlpatterns = [
    path('', views.cart),
    # 加入购物车  分别为商品的id和数量
    path('add/<int:gid>/<int:count>/', views.add),
    # 修改购物车中商品的数量 分别为商品的id和数量
    path('edit/<int:gid>/<int:count>/', views.edit),
    # 删除购物车中的某个商品
    path('delete/<int:gid>/', views.delete),
    path('place_order/', PlaceOrderView.as_view()),
]

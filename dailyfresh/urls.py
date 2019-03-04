"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# 这是要注意是中括号，不是花括号，否则路由+=会报错
urlpatterns = [
    path('admin/', admin.site.urls),
    # 搜索引擎
    path('search/', include('haystack.urls')),
    # 引入users模块路由
    path('users/', include('users.urls', namespace='users')),
    # 引入goods模块路由
    path('', include('goods.urls')),
    # 引入购物车路由
    path('cart/', include('cart.urls')),
]

if settings.DEBUG:  # 配置静态文件路径
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

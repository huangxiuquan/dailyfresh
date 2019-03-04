from django.urls import path
from users.views import RegisterView, LoginView, SiteView
from users import views

# 定义用户模块的路由

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('info/', views.info, name='info'),
    path('order/', views.order, name='order'),
    path('site/', SiteView.as_view(), name='site')
]

app_name = 'users'

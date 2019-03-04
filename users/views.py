from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .models import User, Address
from orders.models import OrderInfo
from goods.models import Goods
import re  # 用于验证邮箱
from django.db import IntegrityError
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from users import user_decorator
from django.core.paginator import Paginator


class RegisterView(View):
    """类视图：处理注册"""

    @staticmethod
    def get(request):
        """处理GET请求，返回注册页面"""
        return render(request, 'users/register.html')

    @staticmethod
    def post(request):
        """处理POST请求，实现注册逻辑"""

        # 获取注册请求参数
        user_name = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 参数校验：缺少任意一个参数，就不要在继续执行
        if not all([user_name, password, email]):
            return redirect(reverse('users/register'))
        # 判断邮箱
        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, 'users/register.html', {'errmsg': '邮箱格式不正确'})
        # 判断是否勾选协
        if allow != 'on':
            return render(request, 'users/register.html', {'errmsg': '没有勾选用户协议'})

        # 保存数据到数据库
        try:
            # 隐私信息需要加密，可以直接使用django提供的用户认证系统完成
            user = User.objects.create_user(user_name, email, password)
        except IntegrityError:
            return render(request, 'users/register.html', {'errmsg': '用户已注册'})

        # 手动的将用户认证系统默认的激活状态is_active设置成False,默认是True
        user.is_active = False
        # 保存数据到数据库
        user.save()
        return render(request, 'users/login.html')


class LoginView(View):
    """类视图：处理登陆"""

    @staticmethod
    def get(request):
        """处理GET请求，返回登陆页面"""
        return render(request, 'users/login.html')

    @staticmethod
    def post(request):
        """处理POST请求，实现登陆逻辑"""

        # 获取注册请求参数
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        jizhu = request.POST.get('jizhu', 0)  # 当jizhu有值时,即jizhu被勾选等于1时,返回的数据为1,否则get返回后面的0

        # 参数校验：缺少任意一个参数，就不要在继续执行
        if not all([username, password]):
            return redirect(reverse('users:login'))

        # 使用自带的auth验证用户（有bug）
        # user = authenticate(username=username, password=password)

        # 根据用户名查询对象
        user = User.objects.get(username=username)

        # 判断：如果未查到则说明用户名错误，如果查到则判断密码是否正确，如果密码正确，则返回用户中心
        if user is None:
            # 响应登录页面，提示用户名不存在
            context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': username, 'upwd': password}
            return render(request, 'users/login.html', context)

        # 验证密码是否正确
        pwd = user.password
        if check_password(password, pwd):
            url = request.COOKIES.get('url', '/')  # 获取登录之前进入的页面,如果没有,则进入首页
            red = HttpResponseRedirect(url)  # 用变量记住,方便设置cookie
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('username', username)  # 设置cookie保存用户名
            else:
                red.set_cookie('username', '', max_age=-1)  # max_age指的是过期时间,当为-1时为立刻过期
            # 使用django的用户认证系统，在session中保存用户的登陆状态
            login(request, user)
            request.session['username'] = username
            request.session['user_id'] = user.id
            # 登陆成功，重定向到主页
            return red
        else:
            # 响应登录页面，提示密码错误
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': username, 'upwd': password}
            return render(request, 'users/login.html', context)


# 收货地址视图
class SiteView(View):
    """类视图，处理收货地址"""

    @staticmethod
    def get(request):
        uid = request.session['user_id']  # 获取用户id
        if uid is None:
            return HttpResponseRedirect('login/')
        addr = Address.objects.filter(user_id=uid)
        address = None
        if len(addr) >= 1:
            address = addr.first()
        context = {'address': address}

        return render(request, 'users/site.html', context)

    @staticmethod
    def post(request):
        uid = request.session['user_id']  # 获取用户id
        if uid is None:
            return HttpResponseRedirect('login/')
        addrs = Address.objects.filter(user_id=uid)
        # 接受参数
        receiver_name = request.POST.get('receiver_name')
        detail_addr = request.POST.get('detail_addr')
        zip_code = request.POST.get('zip_code')
        receiver_mobile = request.POST.get('receiver_mobile')

        # 保存数据到数据库
        try:
            # 如果有地址，则修改
            if len(addrs) >= 1:
                address = addrs.first()
            else:
                address = Address()

            address.receiver_name = receiver_name
            address.detail_addr = detail_addr
            address.zip_code = zip_code
            address.receiver_mobile = receiver_mobile
            address.user_id = uid
            address.save()

            return HttpResponseRedirect("/users/site/")
        except IntegrityError:
            return render(request, 'users/site.html', {'errmsg': '保存失败'})


def logout(request):
    request.session.flush()  # 清空session信息
    return redirect('index')


# 用户中心
@user_decorator.login
def info(request):
    # 用户基本信息
    user = User.objects.get(id=request.session['user_id'])
    # 最近浏览(没有数据支撑，直接去商品)
    goods_list = Goods.objects.all()[:5]
    context = {
        'user': user,
        'goods_list': goods_list
    }
    return render(request, 'users/info.html', context)


# 用户订单
@user_decorator.login
def order(request):
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    # 用户基本信息
    user = User.objects.get(id=request.session['user_id'])
    # 用户所有订单
    order_list = OrderInfo.objects.filter(user_id=user.id)
    paginator = Paginator(order_list, 2)
    orders = paginator.page(page)
    context = {
        'user': user,
        'orders': orders
    }
    return render(request, 'users/order.html', context)

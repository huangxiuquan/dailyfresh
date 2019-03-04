from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from users import user_decorator
from cart.models import CartInfo
from users.models import Address
from django.views import View
from django.db import IntegrityError, transaction
from orders.models import OrderInfo, OrderGoods
from datetime import datetime
import ast


# Create your views here.

@user_decorator.login
def cart(request):  # 购物车
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'page_name': 1,
        'carts': carts,
    }
    return render(request, 'cart/cart.html', context)


# 加入购物车 分别为商品的id和数量
def add(request, gid, count):
    uid = request.session['user_id']  # 获取用户id
    # 没有登录，购物车数量为0
    if uid is None:
        return JsonResponse({'count': 0})
    # 如果商品id和数量都为零，返回历史数据
    if int(gid) == 0 and int(count) == 0:
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count': count})

    gid = int(gid)  # 转化为int型
    count = int(count)
    # 查询购物车中是已有该商品,如果有则数量增加,如果没有则新增一个商品
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)

    if len(carts) >= 1:
        cart_first = carts.first()
        cart_first.count = cart.count + count
        cart_first.save()
    else:
        cart_info = CartInfo()
        cart_info.user_id = uid
        cart_info.goods_id = gid
        cart_info.count = count
        cart_info.save()

    # 如果是ajax请求则返回json,否则转向购物车  测试  正常都不转
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()  # 查询当前登录用户购物车的商品类型数量
        return JsonResponse({'count': count})
    else:
        return HttpResponseRedirect('/cart/')  # 转到购物车


def edit(request, gid, count):
    data = None
    try:
        if request.is_ajax():
            goods = CartInfo.objects.get(id=int(gid))
            goods.count = int(count)
            goods.save()
            data = {'ok': 1}
    except IntegrityError:
        data = {'ok': int(count)}
    return JsonResponse(data)


# 从购物车里删除
def delete(request, gid):
    try:
        cart_info = CartInfo.objects.get(id=int(gid))
        cart_info.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0, 'e': e}
    return JsonResponse(data)


class PlaceOrderView(View):
    """提交订单视图"""

    @staticmethod
    def get(request):
        uid = request.session['user_id']  # 获取用户id
        # None不要赋值给多个
        if uid is None:
            return HttpResponseRedirect('/users/login/')
        # 获取用户地址
        address = Address.objects.filter(user_id=uid)
        if address.count() > 0:
            addr = address.first()
        else:
            addr = ''
        # 获取本次下单商品
        # 这里需要获取参数，暂时先从表里获取所有
        carts = CartInfo.objects.filter(user_id=uid)
        if carts.count() == 0:
            return HttpResponseRedirect('/cart/')

        context = {'addr': addr, 'carts': carts}
        return render(request, 'cart/place_order.html', context)

    @staticmethod
    @transaction.atomic
    def post(request):
        uid = request.session['user_id']  # 获取用户id
        # 先登录
        if uid is None:
            return HttpResponseRedirect('/users/login/')
        # 接受post参数
        address_id = request.POST.get('address_id')  # 收货地址id
        pay_style = request.POST.get('pay_style')  # 支付方式
        card_id = request.POST.get('card_id')  # 购物车商品id
        # 参数校验：缺少任意一个参数，就不要在继续执行
        if not all([address_id, pay_style, card_id]):
            return JsonResponse({'status': 0, 'msg': '缺少参数'})
        # 生成订单
        # 分割字符串为数组
        # 前端增加一个0，为了让下面代码可以执行成功
        cards = ast.literal_eval(card_id)
        try:
            # 开启事物
            with transaction.atomic():
                order_id = '{0:%Y%m%d%H%M%S}'.format(datetime.now())  # 订单号
                # 首先生成订单(先生成订单是为了外键约束)
                order_info = OrderInfo(
                    order_id=order_id,  # 订单号
                    user_id=uid,  # 用户id
                    address_id=address_id,  # 收货地址id
                    total_count=0,  # 商品总数
                    total_amount=0,  # 商品总金额
                    trans_cost=0,  # 运费
                    pay_method=pay_style,  # 支付方式
                    status=1,  # 支付状态
                    create_time=datetime.now()
                )
                order_info.save()
                # 批量插入订单商品
                order_list_to_insert = list()
                total_count = 0
                total_amount = 0
                # 查询
                for cid in cards:
                    if cid == 0:
                        break
                    # 查找购物车id
                    cart_info = CartInfo.objects.get(id=cid)
                    # 添加到订单商品
                    order_list_to_insert.append(OrderGoods(
                        order_id=order_id,  # 关联订单id
                        sku_id=cart_info.goods_id,  # 商品id
                        count=cart_info.count,  # 商品数量
                        price=cart_info.goods.price,  # 商品价格
                        comment='',  # 评论
                        create_time=datetime.now()
                    ))
                    # 计算总数量和总金额
                    total_count += cart_info.count
                    total_amount += cart_info.count * cart_info.goods.price
                    # 从购物车中移除
                    cart_info.delete()
                # 插入订单商品(注意缩进，注意缩进，蛋疼)
                OrderGoods.objects.bulk_create(order_list_to_insert)
                # 更新订单总金额和总数量
                order_info.total_count = total_count
                order_info.total_amount = total_amount
                order_info.save()
            return JsonResponse({'status': 1, 'msg': 'ok'})

        except IntegrityError as e:
            return JsonResponse({'status': 0, 'msg': e.args})

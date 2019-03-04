# template包含了很多与模板有关的类和方法
from django import template

# Library是template类的一个方法
# register包含了simple_tag方法
# 它将用于自定义标签
register = template.Library()


# 表明下面的代码是自定义的simple_tag
# 统计对象个数
@register.simple_tag
def model_count(model):
    return model.count()


# 统计总价格
@register.simple_tag
def total_price(model):
    total = 0
    for item in model:
        summary = item.count * item.goods.price
        total += summary

    return total


# 订单支付状态
@register.filter
def order_status(status):
    status_array = {
        1: "待支付",
        2: "待发货",
        3: "待收货",
        4: "待评价",
        5: "已完成",
    }
    return status_array[status]
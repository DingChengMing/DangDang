from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from cart_app.cart import Cart
from order_app.models import TAddress, TOrder, TOrderitem
from user_app.models import TUser


# Create your views here.
def show_page(request):
    # 强制登录
    email = request.session.get("email")
    if not email:
        return redirect("/userApp/login/page/?flag=order")
    user = TUser.objects.get(email=email)
    # 查询该用户得历史地址
    address = TAddress.objects.filter(user_id=user.id)
    return render(request, "indent.html", {"address": address})


def query_address(request):
    # 查询收货地址
    add_id = request.POST.get("add_id")
    add = TAddress.objects.get(id=add_id)
    return JsonResponse({"name": add.receiver_name, "address": add.address, "number": add.phone, "code": add.zip_code})


def create_order(request):
    # 创建订单
    total_price = float(request.POST.get("total_price"))
    address = request.POST.get("address")
    receiver_name = request.POST.get("name")
    phone = request.POST.get("number")
    email = request.session.get("email")
    user = TUser.objects.get(email=email)
    now_time = str(datetime.now())
    # 生成订单号
    order_id = fun(now_time)+str(user.id)
    order = TOrder.objects.create(order_id=order_id, total_price=total_price, create_time=datetime.now(), user_id=user.id, address=address, status=1, receiver_name=receiver_name, phone=phone)
    # 将session中的cart删除
    del request.session["cart"]
    return HttpResponse(order.id)


def fun(str1):
    # 提取字符串中得所有数字，组成一个新的字符串
    str2 = ''
    for i in str1:
        if i.isdigit():
            str2 += i
    return str2


def create_item(request):
    # 创建订单项
    order_id = int(request.POST.get("order_id"))
    book_id = int(request.POST.get("book_id"))
    amount = int(request.POST.get("amount"))
    subtotal = float(request.POST.get("subtotal"))
    TOrderitem(book_id=book_id, order_id=order_id, book_amount=amount, subtotal=subtotal).save()
    return HttpResponse("1")


def add_cart(request):
    # 将在订单页面移入购物车的重新加入购物车
    book_id = int(request.POST.get("book_id"))
    amount = int(request.POST.get("amount"))
    # 获取session中的购物车
    cart = request.session.get("cart")
    # 判断购物车是否存在
    if cart:
        cart.addCart(book_id, amount)
        request.session["cart"] = cart
    else:
        # 初始化购物车
        cart = Cart()
        # 调用添加方法
        cart.addCart(book_id, amount)
        request.session["cart"] = cart
    return HttpResponse("1")


def add_address(request):
    # 存储收货地址
    man = request.POST.get("man")
    address = request.POST.get("address")
    code = request.POST.get("code")
    number = request.POST.get("number")
    email = request.session.get("email")
    user = TUser.objects.get(email=email)
    TAddress(receiver_name=man, address=address, phone=number, zip_code=code, user_id=user.id).save()
    return HttpResponse('1')


def access(request):
    # 订单页面处理完成之后，跳转至订单完成页面
    order_id = int(request.GET.get("oid"))
    order = TOrder.objects.get(id=order_id)
    price = request.GET.get("pri")
    count = request.GET.get("n")
    return render(request, 'indent ok.html', {"order_id": order.order_id, "price":price, "count": count})

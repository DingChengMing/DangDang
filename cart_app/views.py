from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from cart_app.cart import Cart


# Create your views here.
def showPage(request):
    """
    展示购物车页面
    :return:
    """
    return render(request, 'car.html')


def addCart(request):
    """
    加入购物车模块
    :param request:
    :return:
    """
    # 接收参数
    book_id = int(request.GET.get("book_id"))
    amount = int(request.GET.get("amount"))
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
    return redirect("cartApp:showPage")


def updateCart(request):
    """
    修改购物车项
    :param request:
    :return:
    """
    # 接收参数
    book_id = int(request.POST.get("book_id"))
    amount = int(request.POST.get("amount"))
    cart = request.session.get("cart")
    # 调用方法
    cart.updateCart(book_id, amount)
    # 重新存储一下购物车
    request.session["cart"] = cart
    for i in cart.cartItems:
        if i.book.id == int(book_id):
            price = i.total_price
    return JsonResponse({"item_total_price": price, "total_price": cart.total_price, "save_price": cart.save_price})


def delCart(request):
    """
    删除购物车项
    :param request:
    :return:
    """
    book_id = int(request.POST.get("book_id"))
    if book_id == 0:
        del request.session["cart"]
        return HttpResponse("1")
    cart = request.session.get("cart")
    cart.deleteCart(book_id)
    if cart.cartItems == []:
        del request.session["cart"]
    else:
        request.session["cart"] = cart
    return JsonResponse({"total_price": cart.total_price, "save_price": cart.save_price})


def delPart(request):
    str1 = request.POST.get("book_ids")
    list1 = str1.split(",")
    cart = request.session.get("cart")
    for i in list1:
        if i:
            cart.deleteCart(int(i))
    request.session["cart"] = cart
    return JsonResponse({"total_price": cart.total_price, "save_price": cart.save_price})

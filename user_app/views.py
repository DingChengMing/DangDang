import os
import re

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, HttpResponse, redirect
from user_app.models import TUser
from captcha.image import ImageCaptcha
from django.contrib.auth.hashers import make_password, check_password
import random,string


# Create your views here.
def login_page(request):
    """
    登录页面展示
    :param request:
    :return:
    """
    # 获取请求中的flag，并在展示页面的时候将flag传回，以便在登录处理时使用
    flag = request.GET.get('flag')
    return render(request, 'login.html', {'flag': flag})


def login_logic(request):
    email = request.POST.get("email")
    user = TUser.objects.filter(email=email)
    if user:
        password = user[0].password
        pwd = request.POST.get("pwd")
        if check_password(pwd, password):
            if user[0].status == 1:
                request.session["email"] = email
                return HttpResponse("1")
            else:
                return HttpResponse("2")
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("0")


def login_jump(request):
    flag = request.GET.get("flag")
    save = request.GET.get("save")
    if flag == "index":
        red = redirect("DangDang:main")
    elif flag == "cart":
        red = redirect("cartApp:showPage")
    elif flag == "order":
        red = redirect("orderApp:showPage")
    if save == '1':
        email = request.session.get("email")
        red.set_cookie("email", email, max_age=60*60*24*7)
    else:
        email = request.session.get("email")
        red.delete_cookie("email")
    return red


def regist_page(request):
    """
    注册页面显示
    :param request:
    :return:
    """
    # 获取请求中的flag，并在展示页面的时候将flag传回，以便在注册处理时使用
    flag = request.GET.get('flag')
    return render(request, 'register.html', {'flag': flag})


def mail_check(request):
    """
        邮箱验证
        :param request:
        :return:
        """
    # 获取请求中的邮箱
    mail = request.POST.get('mail')
    # 利用正则检测邮箱的格式是否正确
    rule = "\w+@\w+.\w+"
    re_obj = re.compile(rule, re.X)
    result = re_obj.findall(mail)
    if not result:
        return HttpResponse("邮箱账号格式不正确")
    # 从数据库中查询该邮箱有没有被注册
    user = TUser.objects.filter(email=mail)
    if user:
        return HttpResponse("该邮箱已经注册过当当")
    else:
        return HttpResponse("ok")


def pwd_check(request):
    """
    密码验证
    :param request:
    :return:
    """
    pwd = request.POST.get('pwd')
    a, b, c = 0, 0, 0
    for i in pwd:
        if i.isalpha():
            a = 1
        elif i.isdecimal():
            b = 1
        else:
            c = 1
    if pwd.isalpha() or pwd.isdecimal():
        return HttpResponse('1')
    elif a+b+c == 3:
        return HttpResponse('3')
    else:
        return HttpResponse('2')


def getCaptcha(request):
    """
    验证码模块
    :param request:
    :return:
    """
    # 创建核心类对象，设置字体
    captchaObj = ImageCaptcha(fonts=[os.path.abspath("captcha/segoesc.ttf")])
    # 生成随机码
    captcha = "".join(random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,4))
    print(captcha)
    # 将随机码存入session,供后续验证
    request.session["captcha"] = captcha
    # 根据随机码生成验证码图片
    img = captchaObj.generate(captcha)
    # 写出验证码图片
    return HttpResponse(img, "image/png")


def checkCaptcha(request):
    c1 = request.POST.get("captcha")
    c2 = request.session['captcha']
    if c1.lower() == c2.lower():
        return HttpResponse('ok')
    else:
        return HttpResponse('error')


def regist_logic(request):
    flag = request.GET.get("flag")
    email = request.POST.get("username")
    password = request.POST.get("txt_password")
    password = make_password(password)
    TUser(email=email, password=password, username="用户", status=0).save()
    send_mail(email)
    return render(request, "register ok.html", {"flag": flag, "email": email})


def send_mail(email):
    subject, from_email, to = '当当注册确认', 'dingchengming96@sina.com', email
    text_content = '点击连接进行邮箱验证，验证结束你就可以登录了！'
    html_content = '<p>感谢注册!<a href="http://{}/userApp/regist/confirm/?email={}" target=blank>点击此处</a>，点击连接进行邮箱验证，验证结束你就可以登录了！(为了您的信息安全，如果您没进行注册，请忽略此邮件！) </p> '.format('127.0.0.1:8000', email)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def confirm(request):
    email = request.GET.get("email")
    user = TUser.objects.get(email=email)
    user.status = 1
    user.save()
    return render(request, 'register_confirm.html')


def exit(request):
    """
    退出登录
    :param request:
    :return:
    """
    flag = request.GET.get("flag")
    if request.COOKIES.get("email"):
        if request.session.get("email"):
            del request.session['email']
        if flag == "cart":
            red = redirect("cartApp:showPage")
        else:
            red = redirect("DangDang:main")
        red.delete_cookie("email")
        return red
    elif request.session.get("email"):
        del request.session['email']
        if flag == "cart":
            return redirect("cartApp:showPage")
        else:
            return redirect("DangDang:main")

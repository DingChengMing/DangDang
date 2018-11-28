from _mysql import IntegrityError
from http.client import HTTPResponse

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect
from books_app.models import TBook, TCategory
from order_app.models import TOrder


def index_page(request):
    return render(request, 'manage_sys_temp/index.html')


def add_page(request):
    cates = TCategory.objects.filter(parent_id__gt=0)
    return render(request, 'manage_sys_temp/add.html', {"cates": cates})


def add_logic(request):
    name = request.POST.get("name")
    cname = request.POST.get("cname")
    author = request.POST.get("author")
    press = request.POST.get("press")
    pub_date = request.POST.get("pub_date")
    edition = request.POST.get("edition")
    pri_date = request.POST.get("pri_date")
    impression = request.POST.get("impression")
    isbn = request.POST.get("ISBN")
    num_words = request.POST.get("num_words")
    num_pages = request.POST.get("num_pages")
    size = request.POST.get("size")
    wrap = request.POST.get("wrap")
    market_price = request.POST.get("market_price")
    dang_price = request.POST.get("dang_price")
    content_abstract = request.POST.get("content_abstract")
    author_abstract = request.POST.get("author_abstract")
    directory = request.POST.get("directory")
    commentary = request.POST.get("commentary")
    illustration = request.POST.get("illustration")
    path = request.FILES.get("fengmian")
    shelf_date = request.POST.get("shelf_date")
    score = request.POST.get("score")
    inventory = request.POST.get("inventory")
    sales = request.POST.get("sales")
    category = int(request.POST.get("category"))
    category = TCategory.objects.get(id=category)
    recommend = request.POST.get("recommend")
    # print(name, cname, author, press, pub_date, edition, pri_date, impression, isbn, num_words, num_pages, size, wrap,
    #       market_price, dang_price, content_abstract, author_abstract, directory, commentary, illustration, path,
    #       shelf_date, score, inventory, sales, category, recommend)
    book = TBook.objects.create(name=name, cname=cname, author=author, press=press, pub_date=pub_date, edition=edition,
                         pri_date=pri_date, impression=impression, isbn=isbn, num_words=num_words, num_pages=num_pages,
                         size=size, wrap=wrap, market_price=market_price, dang_price=dang_price,
                         content_abstract=content_abstract, author_abstract=author_abstract, directory=directory,
                         commentary=commentary, illustration=illustration, path=path, shelf_date=shelf_date,
                         score=score, inventory=inventory, sales=sales, category=category, recommend=recommend)
    cate1 = TCategory.objects.get(id=book.category.id)
    cate1.amount += 1
    cate1.save()
    cate2 = TCategory.objects.get(id=book.category.parent_id)
    cate2.amount += 1
    cate2.save()
    return render(request, 'manage_sys_temp/add.html')


def dzlist_page(request):
    num = request.GET.get("num")
    if not num:
        num = 1
    orders = TOrder.objects.all()
    paginator = Paginator(object_list=orders, per_page=6)
    page = paginator.page(num)
    return render(request, 'manage_sys_temp/dzlist.html', {"page": page, "count": orders.count()})


def list_page(request):
    num = request.GET.get("num")
    if not num:
        num = 1
    books = TBook.objects.all()
    paginator = Paginator(object_list=books, per_page=6)
    page = paginator.page(num)
    return render(request, 'manage_sys_temp/list.html', {"page": page, "count": books.count()})


def splb_page(request):
    num = request.GET.get("num")
    if not num:
        num = 1
    cates = TCategory.objects.all()
    paginator = Paginator(object_list=cates, per_page=6)
    page = paginator.page(num)
    return render(request, 'manage_sys_temp/splb.html', {"page": page, "count": cates.count()})


def test_page(request):
    return render(request, 'manage_sys_temp/test.html')


def zjsp_page(request):
    return render(request, 'manage_sys_temp/zjsp.html')


def zisp_logic(request):
    category = request.POST.get("category")
    TCategory.objects.create(name=category, amount=0)
    return redirect('manageApp:zjspPage')


def zjzlb_page(request):
    cates = TCategory.objects.filter(parent_id=None)
    return render(request, 'manage_sys_temp/zjzlb.html', {"cates": cates})


def zjzlb_logic(request):
    category = request.POST.get("category")
    parent_cate = request.POST.get("parent_cate")
    TCategory.objects.create(name=category, parent_id=parent_cate, amount=0)
    return redirect("manageApp:zjzlbPage")


def del_one(request):
    book_id = request.GET.get("id")
    try:
        with transaction.atomic():
            book_id = int(book_id)
            book = TBook.objects.get(id=book_id)
            cate1 = TCategory.objects.get(id=book.category.parent_id)
            cate1.amount -= 1
            cate1.save()
            cate2 = TCategory.objects.get(id=book.category.id)
            cate2.amount -= 1
            cate2.save()
            book.delete()
    except:
        print("事务异常！")
        return render(request, 'manage_sys_temp/error.html')
    return redirect("manageApp:listPage")


def del_many(request):
    ids = request.GET.get("ids")
    list_id = ids.split(",")
    list_id.pop()
    try:
        with transaction.atomic():
            for i in list_id:
                book_id = int(i)
                book = TBook.objects.get(id=book_id)
                cate1 = TCategory.objects.get(id=book.category.parent_id)
                cate1.amount -= 1
                cate1.save()
                cate2 = TCategory.objects.get(id=book.category.id)
                cate2.amount -= 1
                cate2.save()
                book.delete()
    except:
        print("事务异常！")
        return render(request, 'manage_sys_temp/error.html')
    return redirect("manageApp:listPage")



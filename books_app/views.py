from django.core.paginator import Paginator
from django.shortcuts import render


# Create your views here.
from books_app.models import TCategory, TBook


def index(request):
    """
    首页展示
    :param request:
    :return: 首页模板，并传递数据
    """
    # 查询cookie中是否有email，判断是否有用户登录
    # 查询所有分类信息
    category = TCategory.objects.values('id', 'name', 'parent_id', 'amount')
    # 查询新书信息（前8个）
    new_books = TBook.objects.values('id', 'name', 'path', 'author', 'dang_price', 'market_price').order_by('-shelf_date')[:8]
    # 查询主编推荐的图书信息（前8个）
    rec_books = TBook.objects.values('id', 'name', 'path', 'author', 'dang_price', 'market_price').filter(recommend=1).order_by('-shelf_date')[:8]
    # 查询新书热卖的图书信息（前5个）
    hot_books1 = TBook.objects.values('id', 'name', 'path', 'dang_price', 'market_price').order_by('-shelf_date', '-sales')[:5]
    # 查询新书热卖的图书信息（前10个）
    hot_books2 = TBook.objects.values('id', 'name', 'path', 'dang_price', 'market_price').order_by('-sales')[:10]
    return render(request, 'index.html', {'category': category, 'new_books': new_books, 'rec_books': rec_books, 'hot_books1': hot_books1, 'hot_books2': hot_books2})


def details(request):
    """
    图书详情页展示
    :param request:
    :return: 详情页模板，并传递数据
    """
    # 获取请求中的图书id
    id = request.GET.get('id')
    # 根据id查询到对应的书籍信息
    result = TBook.objects.get(id=id)
    # 查询图书的分类信息
    # 一级分类
    category1 = TCategory.objects.get(id=result.category.parent_id)
    return render(request, 'Book details.html', {'book': result, 'category1': category1.name, 'category2':result.category.name})


def book_list(request):
    """
    书籍分类展示页面
    :param request:
    :return: 书籍分类页面模板
    """
    # 获取请求中的分类id和分类父id
    id = int(request.GET.get('id'))
    pid = request.GET.get('pid')

    # 判断是一级分类还是二级分类
    if pid == 'None':
        # 一级分类
        # 查询当前分类的对象
        cate1 = TCategory.objects.get(id=id)
        # 查询当前分类下二级分类的所有对象
        cate2 = TCategory.objects.filter(parent_id=id)
        # 将所有二级分类的id放入一个列表中
        list1 = []
        for i in cate2:
            list1.append(i.id)
        # 查询所有图书分类属于这些二级分类的图书
        books = TBook.objects.filter(category__in=list1)
    else:
        # 二级分类
        # 查询当前分类父分类的对象
        cate1 = TCategory.objects.get(id=pid)
        # 查询分分类下二级分类的所有对象
        cate2 = TCategory.objects.filter(parent_id=cate1.id)
        # 查询当前二级分类下的所有图书
        books = TBook.objects.filter(category=id)

    # 获取请求中的排序的标志
    sort_num = request.GET.get('sort_num')
    # 如果请求中没有sort_num，给sort_num一个默认值
    if not sort_num:
        sort_num = 1
    sort_num = int(sort_num)
    # 根据排序标志对图书信息进行排序
    # 1:默认排序  2：销量降序  3：价格升序  4：出版时间降序
    if sort_num == 1:
        pass
    elif sort_num == 2:
        books = books.order_by('-sales')
    elif sort_num == 3:
        books = books.order_by('dang_price')
    elif sort_num == 4:
        books = books.order_by('-pub_date')

    # 获取请求中的页数
    num = request.GET.get('num')
    # 如果请求中没有num, 给num一个默认值
    if not num:
        num = 1
    # 获取当前页的分页对象
    page = Paginator(object_list=books, per_page=4).page(num)
    return render(request, 'booklist.html', {'current_id': id, 'current_pid': pid, 'cate1': cate1, 'cate2': cate2, 'page': page, 'sort_num': sort_num})

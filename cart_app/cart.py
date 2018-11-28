from books_app.models import TBook


class CartItem():
    def __init__(self, book, amount):
        self.book = book
        self.amount = amount
        self.total_price = 0


class Cart():
    def __init__(self):
        self.total_price = 0
        self.save_price = 0
        self.cartItems = []


    # 添加到购物车
    def addCart(self, book_id, amount):
        for i in self.cartItems:
            if i.book.id == book_id:
                i.amount += amount
                self.sums()
                return
        book = TBook.objects.get(id=book_id)
        self.cartItems.append(CartItem(book, amount))
        self.sums()

    # 计算总价和节省
    def sums(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.cartItems:
            i.total_price = round(i.book.dang_price * i.amount, 2)
            self.total_price = round(self.total_price + i.book.dang_price * i.amount, 2)
            self.save_price = round(self.save_price + (i.book.market_price - i.book.dang_price) * i.amount, 2)

    # 更新购物车
    def updateCart(self, book_id, amount):
        for i in self.cartItems:
            if i.book.id == book_id:
                i.amount = amount
        self.sums()

    # 删除购物车项
    def deleteCart(self, book_id):
        for i in self.cartItems:
            if i.book.id == book_id:
                self.cartItems.remove(i)
        self.sums()

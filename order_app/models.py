from django.db import models
from books_app.models import TBook
from user_app.models import TUser


# Create your models here.
class TAddress(models.Model):
    receiver_name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    zip_code = models.CharField(max_length=6)
    user = models.ForeignKey(TUser, models.DO_NOTHING)

    class Meta:
        db_table = 't_address'


class TOrder(models.Model):
    order_id = models.CharField(max_length=32)
    total_price = models.FloatField()
    create_time = models.DateTimeField()
    user = models.ForeignKey(TUser, models.DO_NOTHING)
    address = models.CharField(max_length=100)
    status = models.IntegerField()
    receiver_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)

    class Meta:
        db_table = 't_order'


class TOrderitem(models.Model):
    book = models.ForeignKey(TBook, models.DO_NOTHING)
    order = models.ForeignKey(TOrder, models.DO_NOTHING)
    book_amount = models.IntegerField()
    subtotal = models.FloatField()

    class Meta:
        db_table = 't_orderitem'
from django.db import models


# Create your models here.
class TBook(models.Model):
    name = models.CharField(max_length=20)
    cname = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    press = models.CharField(max_length=20)
    pub_date = models.DateTimeField()
    edition = models.IntegerField()
    pri_date = models.DateTimeField()
    impression = models.IntegerField()
    isbn = models.CharField(db_column='ISBN', max_length=64)  # Field name made lowercase.
    num_words = models.IntegerField()
    num_pages = models.IntegerField()
    size = models.IntegerField()
    wrap = models.CharField(max_length=20)
    market_price = models.FloatField()
    dang_price = models.FloatField()
    content_abstract = models.CharField(max_length=2000)
    author_abstract = models.CharField(max_length=2000)
    directory = models.CharField(max_length=2000)
    commentary = models.CharField(max_length=2000)
    illustration = models.CharField(max_length=2000)
    path = models.ImageField(upload_to="book_images", default="huozhe.jpg")
    shelf_date = models.DateTimeField()
    category = models.ForeignKey('TCategory', models.DO_NOTHING, db_column='category')
    score = models.FloatField()
    inventory = models.IntegerField()
    sales = models.IntegerField()
    recommend = models.IntegerField(null=True)

    class Meta:
        db_table = 't_book'


class TCategory(models.Model):
    name = models.CharField(max_length=20)
    parent_id = models.IntegerField(null=True)
    amount = models.IntegerField()

    class Meta:
        db_table = 't_category'
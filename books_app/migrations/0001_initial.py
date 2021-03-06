# Generated by Django 2.0.2 on 2018-11-26 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('cname', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=20)),
                ('press', models.CharField(max_length=20)),
                ('pub_date', models.DateTimeField()),
                ('edition', models.IntegerField()),
                ('pri_date', models.DateTimeField()),
                ('impression', models.IntegerField()),
                ('isbn', models.CharField(db_column='ISBN', max_length=64)),
                ('num_words', models.IntegerField()),
                ('num_pages', models.IntegerField()),
                ('size', models.IntegerField()),
                ('wrap', models.CharField(max_length=20)),
                ('market_price', models.FloatField()),
                ('dang_price', models.FloatField()),
                ('content_abstract', models.CharField(max_length=2000)),
                ('author_abstract', models.CharField(max_length=2000)),
                ('directory', models.CharField(max_length=2000)),
                ('commentary', models.CharField(max_length=2000)),
                ('illustration', models.CharField(max_length=2000)),
                ('path', models.ImageField(default='huozhe.jpg', upload_to='book_images')),
                ('shelf_date', models.DateTimeField()),
                ('score', models.FloatField()),
                ('inventory', models.IntegerField()),
                ('sales', models.IntegerField()),
                ('recommend', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 't_book',
            },
        ),
        migrations.CreateModel(
            name='TCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('parent_id', models.IntegerField(null=True)),
                ('amount', models.IntegerField()),
            ],
            options={
                'db_table': 't_category',
            },
        ),
        migrations.AddField(
            model_name='tbook',
            name='category',
            field=models.ForeignKey(db_column='category', on_delete=django.db.models.deletion.DO_NOTHING, to='books_app.TCategory'),
        ),
    ]

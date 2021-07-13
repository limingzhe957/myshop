from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# 用户表
class User2(models.Model):
    username = models.CharField(primary_key=True, max_length=20, verbose_name='账号')
    password = models.CharField(max_length=20, verbose_name='密码')
    email = models.EmailField()

# 用户表
class User(AbstractUser, models.Model):
    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


# 商品表
class Product(models.Model):
    product_name = models.CharField(max_length=48, verbose_name='商品名')
    product_introduce = models.TextField(verbose_name='简介')
    product_num = models.IntegerField(verbose_name='商品剩余数量')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    product_picture = models.FileField(verbose_name='商品图片', upload_to='static/img/good', default='')
    product_class = models.ForeignKey('ProductClass', verbose_name='种类名', on_delete=models.CASCADE)


# 种类表
class ProductClass(models.Model):
    product_class_name = models.CharField(max_length=48, verbose_name='种类名')


# 收藏表（这个应该用redis）因为查太多数据库会增加
class Collect(models.Model):
    username = models.CharField(max_length=20,verbose_name='用户名')
    save_id = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='存的商品id',null=True)

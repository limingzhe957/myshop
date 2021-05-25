from django.db import models

# Create your models here.

#用户表
class User2(models.Model):
    username = models.CharField(primary_key=True, max_length=20, verbose_name='账号')
    password = models.CharField(max_length=20, verbose_name='密码')
    email = models.EmailField()

#商品表
class Goods(models.Model):
    good_id = models.AutoField(primary_key=True, verbose_name='商品id')
    good_name = models.CharField(max_length=20,verbose_name='商品名')
    good_introduce = models.TextField(verbose_name='简介')
    good_num = models.IntegerField(verbose_name='商品剩余数量')
    good_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    good_picture = models.FileField(verbose_name='商品图片', upload_to='static/img/good', default='')



#收藏表（这个应该用redis）因为查太多数据库会增加
class Collect(models.Model):
    collect_id = models.AutoField(primary_key=True,verbose_name='收藏id')
    username = models.CharField(max_length=20,verbose_name='用户名')
    save_id = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='存的商品id',null=True)

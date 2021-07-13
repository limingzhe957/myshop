from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from user.models import Collect, Product, ProductClass
from django.core.paginator import Paginator
from util.mixin import LoginRequiredMixin
# Create your views here.


# 商品种类添加
class AddClassView(View):
    def get(self, request):
        return render(request, 'add_class.html')

    def post(self, request):
        classname = request.POST.get('classname')
        print(classname)
        try:
            ProductClass.objects.get(product_class_name=classname)
            return render(request, 'add_class.html', {'errmsg': '该类别已存在'})
        except:
            ProductClass.objects.create(product_class_name=classname)
            return render(request, 'add_class.html', {'errmsg': '添加成功'})


# 商品添加
class AddView(View):
    """添加功能"""
    def get(self, request):
        '''页面显示'''
        product_class = ProductClass.objects.all()
        context = {'product_class': product_class}
        return render(request, 'add_shangpin.html', context)

    def post(self, request):
        # 接收数据
        product_name = request.POST.get('name')
        product_introduce = request.POST.get('introduce')
        product_num = request.POST.get('num')
        product_price = request.POST.get('price')
        product_picture = request.FILES.get('img')
        product_class = request.POST.get('product_class')

        # 处理数据
        # 判断数据是否全
        if not all([product_name, product_introduce, product_num, product_price, product_picture, product_class]):
            return render(request, 'add_shangpin.html', {'errmsg': '数据不完整'})

        product_class = ProductClass.objects.get(product_class_name=product_class)
        # 存入数据库
        Product.objects.create(product_name=product_name, product_introduce=product_introduce, product_num=product_num,
                             product_price=product_price, product_picture=product_picture, product_class=product_class)

        return HttpResponse('存入成功')


# 商品列表页 /list/list/page
class ListView(View):

    def get(self, request, page):
        uid = request.session.get('uid')
        Products = Product.objects.all()

        # 生成paginator对象,定义每页显示1条记录
        paginator = Paginator(Products, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages+1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages-4, num_pages+1)
        else:
            pages = range(page-2, page+3)

        # 获取第page页的Page实例对象
        product_page = paginator.page(page)

        context_data = {
            'uid': uid,
            'product_page': product_page,
            'pages': pages
        }

        return render(request, 'list.html', context_data)


# 收藏
class CollectView(View):
    def get(self, request, good_id):

        uid = request.session.get('uid')
        if not uid:
            return redirect('user:login')

        # #判断收藏表里是否有改收藏
        # collect = Collect.objects.get(save_id=good_id)
        # if collect:
        #     return HttpResponse('你已经收藏')
        # else:
        one_link = Product.objects.get(good_id=good_id)
        Collect.objects.create(username=uid, save_id_id=one_link.good_id)

        return redirect('list:collect_list')
        # one_link = Goods.objects.get(good_id=good_id)
        # Collect.objects.create(username=uid, save_id_id=one_link.good_id)
        #
        # return redirect('list:collect_list')


# 收藏页
class Collect_listView(View):

    def get(self, request):
        uid = request.session.get('uid')
        # print(uid)

        # save1 = Goods.objects.all()
        # save2 = Collect.objects.get(username=uid)
        # save3=save2.goods_set.all()
        # print(save3)
        # select * from Goods where (good_id = select good_id from collect where username= uid )
        # save2 = Collect.objects.get(username=uid)
        # Goods.objects.filter()
        # list= []
        # list1=[]
        # dict= {}
        # # for i in save:
        # #     s=i.save_id
        # #     list.append(s)
        # # print(list)
        # # for a in set(list):
        # #     GOODS=Goods.objects.filter(good_id=a)
        # #     list1.append(GOODS)
        # # print(list1)
        # #
        # # print(save)
        # 查了good_id的列表
        good_id_list = Collect.objects.filter(username=uid).values_list('save_id', flat=True)

        good_list = []
        for good_id in good_id_list:
            a = Product.objects.filter(good_id=good_id).first()
            good_list.append(a)

        # Goods.objects.filter()
        context_data = {
            'good_list': good_list

        }

        return render(request, 'collect_list.html', context_data)


# 删除收藏
class Collect_list_deleteView(View):

    def get(self, request, good_id):

        uid = request.session.get('uid')
        if not uid:
            return redirect('user:login')

        one_link = Product.objects.get(good_id=good_id)
        Collect.objects.filter(username=uid, save_id_id=one_link.good_id).delete()

        return redirect('list:collect_list')











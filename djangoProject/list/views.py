from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from user.models import Goods, Collect
from django.core.paginator import Paginator
from util.mixin import LoginRequiredMixin
# Create your views here.

#商品添加
class AddView(View):
    """添加功能"""
    def get(self,request):
        '''页面显示'''
        return render(request,'add_shangpin.html')
    def post(self,request):
        #接收数据
        good_name = request.POST.get('name')
        good_introduce = request.POST.get('introduce')
        good_num = request.POST.get('num')
        good_price = request.POST.get('price')
        good_picture = request.FILES.get('img')


        #处理数据
        # 判断数据是否全
        if not all([good_name, good_introduce, good_num, good_price, good_picture]):
            return render(request, 'add_shangpin.html', {'errmsg': '数据不完整'})

        #存入数据库
        Goods.objects.create(good_name=good_name, good_introduce=good_introduce, good_num=good_num,
                             good_price=good_price, good_picture=good_picture)

        return HttpResponse('存入成功')


#商品列表页 /list/list/page
class ListView(View):
    def get(self, request, page):

        uid = request.session.get('uid')
        GOOD = Goods.objects.all()

        # 生成paginator对象,定义每页显示1条记录
        paginator = Paginator(GOOD, 1)

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
        good_page = paginator.page(page)

        context_data = {
            'uid': uid,
            'good_page': good_page,
            'pages': pages
        }

        return render(request, 'list.html', context_data)


#收藏
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
        one_link = Goods.objects.get(good_id=good_id)
        Collect.objects.create(username=uid, save_id_id=one_link.good_id)

        return redirect('list:collect_list')

        # one_link = Goods.objects.get(good_id=good_id)
        # Collect.objects.create(username=uid, save_id_id=one_link.good_id)
        #
        # return redirect('list:collect_list')


#收藏页
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
        #查了good_id的列表
        good_id_list = Collect.objects.filter(username=uid).values_list('save_id', flat=True)

        good_list = []
        for good_id in good_id_list:
            a= Goods.objects.filter(good_id=good_id).first()
            good_list.append(a)

        # Goods.objects.filter()
        context_data = {
            'good_list': good_list

        }

        return render(request, 'collect_list.html', context_data)


#删除收藏
class Collect_list_deleteView(View):
    def get(self, request, good_id):

        uid = request.session.get('uid')
        if not uid:
            return redirect('user:login')

        one_link = Goods.objects.get(good_id=good_id)
        Collect.objects.filter(username=uid, save_id_id=one_link.good_id).delete()

        return redirect('list:collect_list')











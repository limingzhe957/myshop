import re

from django.contrib.auth import login
from user.models import User
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.views.generic import View
# Create your views here.


# 注册
class RegisterView(View):
  '''注册'''
  def get(self, request):
    '''显示'''
    return render(request, 'register.html')

  def post(self,request):
    '''进行注册处理'''
    # 接受数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    cpassword = request.POST.get('cpwd')
    email = request.POST.get('email')

    # 数据处理
    # 判断密码是否一致
    if password != cpassword:
      return render(request, 'register.html', {'errmsg': '前后密码不一致'})
    # 判断数据是否全
    if not all([username, password, cpassword, email]):
      return render(request, 'register.html', {'errmsg': '数据不完整'})
    # 判断邮箱是否匹配
    if not re.match(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', email):
      return render(request, 'register.html', {'errmsg': '邮箱不正确'})
    # 判断是否有该用户
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      user = None
    if user:
      return render(request, 'register.html', {'errmsg': '用户名已存在'})
    #存数据库
    user = User.objects.create_user(username, password, email)
    user.save()

    return HttpResponse('注册成功')


# 校验
class FormExa(View):
  def get(self, request):
    '''显示'''
    return render(request, 'register1.html')


# 登录
class LoginView(View):
  '''登录'''
  def get(self,request):
    '''显示页面'''
    return render(request, 'login.html')
  def post(self,request):
    '''登录页面'''

    #数据接收
    username = request.POST.get('username')
    password = request.POST.get('pwd')

    #数据处理
    if not all([username,password]):
      return render(request, 'login.html', {'errmsg': '数据不完整'})

    #查数据库中是否有改用户
    try:
      user = User.objects.get(username=username)
    except:
      return render(request, 'login.html', {'errmsg': '用户或密码错误'})
    # 判断用户密码是否正确
    try:
      psw = User.objects.get(username=username,password=password)
    except:
      return render(request, 'login.html', {'errmsg': '用户或密码错误'})
    # response.set_cookie('name', username)  # 使用response（用户自己电脑）保存的cookie来验证用户登录
    # 存入缓存
    request.session['uid'] = user.username



    return redirect('list:list', 1)
    # return render(request, 'list.html', {'username': username})

#退出
class LogoutView(View):
  def get(self, request):

      request.session.clear()

      return redirect('list:list', 1)









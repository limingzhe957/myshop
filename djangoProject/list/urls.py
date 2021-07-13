from django.urls import path
from list import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path(r'add_good/', views.AddView.as_view(), name='add_good'),  # 商品增加
    path(r'add_class', views.AddClassView.as_view(), name='add_class'),  # 种类添加
    path(r'list/<page>/', views.ListView.as_view(), name='list'),  # 商品列表
    path(r'collect/<good_id>/', views.CollectView.as_view(), name='collect'),  # 商品收藏
    path(r'collect_list', views.Collect_listView.as_view(), name='collect_list'),  # 收藏列表页
    path(r'collect_list/<good_id>', views.Collect_list_deleteView.as_view(), name='collect_list_delete'),  # 收藏列表页
]+static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS)

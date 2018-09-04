"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# blog/urls
"""
此路径下的urls只用于blog相关的urls配置
需要在主程序的urls.py下用include方法导入当前urls配置

"""
from django.conf.urls import url
from django.contrib import admin
from blog import views

# 视图函数命名空间,告诉Django这个urls.py模块是属于blog应用的,避免多个名为index的冲突
app_name = 'blog'
# url和函数关系
urlpatterns = [
    # url(网址,处理函数)
    # django正则会去掉协议 域名 端口号,然后开始正则
    url(r'^admin/', admin.site.urls),
    # 视图函数写法
    # url(r'^$',views.index,name='index'),
    # 转换类视图函数为视图函数 as_view()将类转换为视图函数
    url(r'^$',views.IndexView.as_view(),name='index'),
    # 先获取用户点击的post-id,捕获得到post/255/ ,再将捕获到的参数传到视图函数detail中
    # url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # 详情 类视图函数写法
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    # 正则归档年月archives(request, year=2017, month=3)
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    # 归档的 类视图函数写法
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    # 正则获取分类id,进入只有该类的全部文章页面
    # url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category'),
    # 分类的 类视图函数写法
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$',views.TagView.as_view(),name='tag'),
    # 简单搜索功能
    # url(r'^search/$', views.search, name='search'),
]















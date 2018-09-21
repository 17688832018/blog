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
from django.conf.urls import url,include
from django.contrib import admin
from blog.feeds import AllPostRssFeed

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # 导入app中的urls配置 会拼接两个urls字符串 即主程序中的r'pro/'+应用中urls中的r'blog/' = 'pro/blog'
    # namespace和app_name用于跟blog/urls的app_name='blog'对应(django1.8版本需要)
    url(r'',include('blog.urls',namespace='blog',app_name='blog')),
    url(r'',include('comments.urls')),
    url(r'^all/rss/$',AllPostRssFeed(),name='rss'),
    # haystack搜索引擎
    url(r'^search/', include('haystack.urls')),
]

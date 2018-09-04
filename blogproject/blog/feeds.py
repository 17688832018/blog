# !-*-coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from .models import Post

"""
聚合阅读器
指定要生成的 XML 文档内容。各个属性和方法的含义已在代码中注释，
你只需把相关的内容替换成符合你博客的描述即可。
"""
class AllPostRssFeed(Feed):
    title= "我的Django博客"
    # 通过聚合阅读器跳转到网站的地址
    link= "/"
    description="这是显示在聚合阅读器上的描述信息"
    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()
    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category,item.title)
    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body

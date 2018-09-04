#!-*-coding:utf-8 -*-
from django import template
from ..models import Post, Category, Tag
# 引入Count,在 Django ORM 中是保存到 Category 的实例的属性中，每个实例对应一条记录
from django.db.models.aggregates import Count
"""
页面侧边栏逻辑

将函数 get_recent_posts 装饰为 register.simple_tag模板标签(django固定格式)
这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了,不写在模板就不能直接调用
"""
register = template.Library()
# 获取最近的5条文章列表 返回整个文章列表对象(包含时间 内容 作者等)
@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

# 归档模板标签(比如2月 1月) 返回date格式对象
@register.simple_tag
def archives():
    # dates('按照排序','精度',顺序)
    return Post.objects.dates('created_time','month',order='DESC')

# 分类模板标签  返回类别对象
@register.simple_tag
def get_categories():
    # return Category.objects.all()
    """
    annotate 方法不局限于用于本文提到的统计分类下的文章数，你也可以举一反三，
    只要是两个 model 类通过 ForeignKey 或者 ManyToMany 关联起来，
    那么就可以使用 annotate 方法来统计数量
    """
    # 使用annotate获取每个分类目录下的文章记录数 类似于.all(),但同时它还会做一些额外的事情
    #                                          'post'的数量.过滤掉post条数为0的分类不显示
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 标签云
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)






















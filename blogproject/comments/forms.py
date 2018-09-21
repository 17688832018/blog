#!-*-coding:utf-8 -*-
from django import forms
from .models import Comment

"""
Django 的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类。
如果表单对应有一个数据库模型（例如这里的评论表单对应着评论模型），
那么使用 ModelForm 类会简单很多 

不用写数据库操作:
 Django 的 ORM 系统内部帮我们做了一些事情。我们遵循 Django 的规范
 写的一些 Python 代码，例如创建 Post、Category 类，然后通过运行数据库迁移命令将这些代码反应到数据库
"""
class CommentForm(forms.ModelForm):
    class Meta:
        # 表明该表单对应的数据库模型为Comment
        model = Comment
        # 必须为fields 需要显示的字段
        fields = ['name','email','url','text']














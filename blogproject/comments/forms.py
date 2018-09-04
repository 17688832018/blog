#!-*-coding:utf-8 -*-
from django import forms
from .models import Comment

"""
Django 的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类。
如果表单对应有一个数据库模型（例如这里的评论表单对应着评论模型），
那么使用 ModelForm 类会简单很多
"""
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 必须为fields
        fields = ['name','email','url','text']














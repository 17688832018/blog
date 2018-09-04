#!-*-coding:utf-8 -*-
from django.conf.urls import  url
from . import views


app_name = 'comments'
urlpatterns = [
    # 此处邮箱正则有bug
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$',views.post_comment,name='post_comment'),
]








"""评论模块 模型"""
from django.db import models
from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    # 创建评论时间为当前系统时间,应改为utc/网络 时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 一篇文章可有多个评论(用外键)
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]




















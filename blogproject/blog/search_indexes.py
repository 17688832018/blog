# !-*-coding:utf-8 -*-
from haystack import indexes
from .models import Post
"""
这是 django haystack 的规定。要相对某个 app 下的数据进行全文检索，
就要在该 app 下创建一个 search_indexes.py 文件，然后创建一个XXIndex类
（XX为含有被检索数据的模型,如这里的Post）并且继承SearchIndex和Indexable
"""

class PostIndex(indexes.SearchIndex,indexes.Indexable):
    # 使用该text作为索引内容
    text = indexes.CharField(document=True,use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


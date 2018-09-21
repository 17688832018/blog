"""存放模型,继承自modles.Model
创建了3个模型(表),类别表 标签表 文章表
文章表中包含类别和标签属性,用foreignKey和manyToManyField关联这两个类别表和标签表
更新模型后 要在python manage.py 中更新
"""
from django.db import models
# django内置应用
from django.contrib.auth.models import User
# python_2_unicode_compatible 装饰器用于兼容 Python2
from django.utils.six import python_2_unicode_compatible
# 调用urls的获取路径的方法
from django.urls import reverse
# 调用markdown
import markdown
# 调用去除html文本中的html标签
from django.utils.html import strip_tags


# python2用unicode替代str方法
# 文章分类
@python_2_unicode_compatible
class Category(models.Model):
    # 超出长度无法存入到数据库
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
# 文章标签类
@python_2_unicode_compatible
class Tag(models.Model):
    name =models.CharField(max_length=100)
    def __str__(self):
        return self.name
# 文章内容类
@python_2_unicode_compatible
class Post(models.Model):

    # 实例化对象
    # 文章标题 CharField()默认不能为空
    title =models.CharField(max_length=70)
    # 文章正文  内容较长的文本用TextField()
    body =models.TextField()
    # 文章创建时间  存储时间字段用DateTimeField() 在shell里赋值为timezone.now()
    created_time =models.DateTimeField()
    # 文章最后修改时间
    modified_time =models.DateTimeField()
    # 文章摘要  允许空值
    excerpt =models.CharField(max_length=200,blank=True)
    # 实例化分类(一篇文章只能有一个分类 一对多用ForeignKey()) 不为空
    category =models.ForeignKey(Category)
    # 实例化标签(一篇文章可有多个标签,一个标签也可对应多个文章,多对多用ManyToManyField())
    tags =models.ManyToManyField(Tag,blank=True)
    # 作者  使用django内置应用
    author =models.ForeignKey(User)
    # 阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # 自定义排序,在视图函数中就不用排序了
    class Meta:
        ordering = ['-created_time']

    """ 1.reverse的'blog:detail'对应blog应用下的name='detail'的方法(对应urls.py的name)
        2.reverse()方法会去解析'blog:detail'的url,解析规则是根据urls.py里的正则.
        3.根据正则规则,解析结果为post/255/,这样Post自己就生成了自己的url
        4.kwargs表示按照关键字传值将多余的传值用字典形式呈现
    """
    # 自定义获取路径方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 阅读量增加(粗略统计,同时访问被忽略)
    def increase_views(self):
        # 该函数每被调用一次 views+1
        self.views +=1
        # 只更新数据库中views字段的值
        self.save(update_fields=['views'])

    # 摘要逻辑 重写save()方法,保存到数据库之前进行一次过滤
    def save(self, *args, **kwargs):
        # 如果没填写摘要
        if not self.excerpt:
            # 实例化一个Markdown对象,用于渲染body的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的 save 方法将数据保存到数据库中
        # 这里save不能有self参数(不能在模型保存中强制更新和插入)
        super(Post,self).save(*args, **kwargs)
    """或者可用模板过滤器(filter) 
    例如:<p> {{ post.body|truncatechars:54 }} </p>
    # 将会显示文章内容的前54个字节,若文章前54字节包含html标签,仍将作为摘要会显示
    """











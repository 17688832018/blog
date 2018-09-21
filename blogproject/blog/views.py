import markdown

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag
# 引入markdown
import markdown
# 引入评论CommentForm
from comments.forms import CommentForm
# django 的类视图函数写法
from django.views.generic import ListView,DetailView
# 美化锚点链接的url
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# 搜索功能
from django.db.models import Q

# def index(request):
    # return HttpResponse("欢迎访问我的博客首页!")
    # render(request,模板名,context={})
    # 逆序排序获得全部文章
    # post_list=Post.objects.all().order_by('-created_time')
    # return render(request,'blog/index.html',context={
    # # title welcome 对应模板里的{{title}} {{welcome}}
        # 'title':'我的博客首页',
        # 'welcome':'欢迎访问我的博客首页',
        # 'post_list':post_list
    # })


# 首页视图函数def
# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

# 简单搜索
def search(request):
    # 获取模板中name='q' 即用户搜索的关键词
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键字"
        return render(request,'blog/index.html',{'error_msg':error_msg})
    # 过滤器:要过滤的属性title和body + __ +i前缀(不区分大小写) + contains(包含)
    # 用Q对象和| 实现或效果
    #如果不用 Q 对象,就只能写成title__icontains=q,body__icontains=q,这是且关系
    post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
    return render(request,'blog/index.html',{'error_msg':error_msg,
                                             'post_list':post_list})


"""首页视图(django类视图函数写法)
 继承某个类视图,ListView用于从数据库获取模型列表数据,所以此处继承ListView
 之后在urls中将该类转换为视图函数def
"""
class IndexView(ListView):
    # 告诉ListView我们要获取的模型是Post
    model = Post
    # 指定这个视图渲染的模板
    template_name = 'blog/index.html'
    # 获取到的列表数据保存到这个变量名中
    context_object_name = 'post_list'
    # 激活分页 如:每页显示2条博客
    paginate_by = 2

    def get_queryset(self):
        return super(IndexView,self).get_queryset().order_by('-created_time')

    # 详细分页
    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

# 详情视图
# def detail(request,pk):
#     # 调用系统方法,有就正常返回,没有则404
#     post=get_object_or_404(Post,pk=pk)
#     # 阅读量+1
#     post.increase_views()
#     '''
#     允许markdown:
#     1.install markdown和pygments
#     2.django过滤器设置,模板中{{post.body|safe}}
#     3.引入高亮css
#     4.编写逻辑:渲染html再传递给模板
#     文章存在post.body中,对其进行markdown渲染后再传递给模板
#     说明:extra包含很多扩展,codehilite语法高亮提示,toc允许生成目录
#     '''
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                      'markdown.extensions.extra',
#                                      'markdown.extensions.codehilite',
#                                      'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     # 获取这篇post下的全部评论
#     comment_list = post.comment_set.all()
#     # 将文章/表单/评论列表作为模板变量传给detail.html模板
#     context = {'post':post,
#                'form':form,
#                'comment_list':comment_list}
#     return  render(request,'blog/detail.html',context=context)
#     # return render(request, 'blog/detail.html', context={'post': post})

# 详情视图的 类视图函数写法
class PostDetailView(DetailView):
    model=Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView,self).get(request,*args,**kwargs)
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
       # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        # post = super(PostDetailView, self).get_object(queryset=None)
        # post.body = markdown.markdown(post.body,
        #                               extensions=[
        #                                   'markdown.extensions.extra',
        #                                   'markdown.extensions.codehilite',  # 高亮拓展
        #                                   'markdown.extensions.toc',  # 目录拓展
        #                               ])
        # 用markdown渲染文章目录侧边栏
        post = super(PostDetailView, self).get_object(queryset=None)
        # 先创建一个markdown.Markdown的实例化对象
        """
        和之前不同的是，extensions中的toc拓展不再是字符串markdown.extensions.toc ，
        而是TocExtension的实例.TocExtension在实例化时其slugify参数可以接受一个函数作为参数，
        这个函数将被用于处理标题的锚点值。Markdown 内置的处理方法不能处理中文标题，
        所以我们使用了 django.utils.text 中的 slugify 方法，该方法可以很好地处理中文。
        """
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            # 让markdown锚点可处理中文
            TocExtension(slugify=slugify)
        ])
        # 使用该实例的convert方法将post.body中的Markdown文本渲染成HTML文本
        post.body = md.convert(post.body)
        """
        而一旦调用该方法后，实例 md 就会多出一个 toc 属性，这个属性的值就是内容的目录，
        我们把 md.toc 的值赋给 post.toc 属性（要注意这个 post 实例本身是没有 md 属性的，
        我们给它动态添加了 md 属性，这就是 Python 动态语言的好处，
        不然这里还真不知道该怎么把 toc 的值传给模板
        """
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


# 归档视图(位于右侧)
"""
请求响应流程:
1.加载页面:模板页面中 调用模板标签显示归档的date.year和date.month 位于templatetags/blog_tags中的archives(精确到月,逆序)
2.发送请求:点击页面的a标签的href="{% url 'blog:archives' date.year date.month %}链接后,到urls.py中进行路由(blog应用的name=archives的url)
    例如发送请求/archives/2018/8/
3.获取请求:获得/archives/2018/8/路径,并且路由到views的archives(传递了年和月两个参数)进行逻辑处理,
4.处理请求:将某月档下的博客响应到前台 

通过过滤器filter排序 不用获得全部的Post.objects.all()
用于python类中调用的created_time.year作为参数列表时被替换为created_time__year

"""
"""
pytz作用
解决归档不到时区
filter 时同时出现 year、month 无法查询的问题

建议数据库使用 UTC 时间 (django.utils.timezone.now())，而不是本地时间（datetime.datetime.now()），
本地时间由 Django 自动转换。这样方便后期修改时区。
设置 settings.py 文件，配置 USE_TZ=True，即启用 UTC 时间。
解决 filter 时同时出现 year、month 无法查询的问题
不同数据库需求不一样
SQLite: install pytz — conversions are actually performed in Python.  
PostgreSQL: no requirements (see Time Zones).  
Oracle: no requirements (see Choosing a Time Zone File).  
MySQL: install pytz and load the time zone tables with mysql_tzinfo_to_sql.安装完 pytz 后，MySQL 需要导入时区 
Linux 和 MacOS： 
sudo mysql_tzinfo_to_sql /usr/share/zoneinfo/ | mysql -u root mysql 
Windows
先停止 mysqld.exe，到 https://dev.mysql.com/downloads/timezones.html 下载对应版本的时区文件，
覆盖 mysql 安装目录下的 data\mysql 文件夹下的同名文件，重新启动 mysql.exe。
"""
# 归档视图(位于右侧)
# def archives(request,year,month):
#     post_list=Post.objects.filter(created_time__year=year,
#                                   created_time__month=month)
#                                   # ).order_by('-created_time')
#     return render(request,'blog/index.html',context={'post_list': post_list})

# 归档的类视图函数写法
class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        # 先获取模板的year
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(created_time__year=year,
                                                              created_time__month=month)

# 分类的类视图函数写法
# def category(request, pk):
#     # 根据pk值在数据库中获取到该分类,
#     cate=get_object_or_404(Category, pk=pk)
#     # 再通过filter获取到该分类下的所有文章 过滤Post.object里的category等同页面获取到的分类cate
#     post_list = Post.objects.filter(category=cate)
#     # post_list=Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})


"""
从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里,
非命名组参数值保存在实例的 args 属性（是一个列表）里
"""
# 类视图函数写法 分类 由于本类指定的属性值和IndexView一样,所以可以继承上面的IndexView
class CategoryView(IndexView):
    # 重写父类方法,默认取指定模型的全部列表数据,加过滤器
    def get_queryset(self):
        cate =get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

# 类视图函数写法 标签
class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

























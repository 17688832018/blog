from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm


def post_comment(request,post_pk):
    # 当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户
    post=get_object_or_404(Post,pk=post_pk)
    # 如果form提交方式为post:
    if request.method =='POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象
        # 我们利用这些数据构造了CommentForm的实例，这样Django的表单就生成了。
        form = CommentForm(request.POST)
        # 若数据合法
        if form.is_valid():
            # 则生成表单的实例comment(里面包含评论/时间/作者),不保存到数据库
            comment=form.save(commit=False)
            # 将评论和被评论的文章关联起来
            comment.post = post
            # 调用模型实例的 save 方法保存到数据库
            comment.save()
            # 重定向到 post 的详情页
            # 然后重定向到 get_absolute_url 方法返回的 URL
            return redirect(post)
        # 若数据不合法:
        else:
            # 获取这篇 post 下的的全部评论
            comment_list=post.comment_set.all()
            context={'post':post,
                     'form':form,
                     'comment_list':comment_list
                     }
            return render(request,'blog/detail.html',context=context)
    return redirect(post)



"""通过python manage.py createsuperuser创建超级用户后,在这里注册模型"""
from django.contrib import admin
from .models import Post,Category,Tag

# 为admin界面添加一个列表
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


# 注册模型
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(PostAdmin)


from django.contrib import admin
from .models import Post,Category,Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


# 注册模型
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(PostAdmin)

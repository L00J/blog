from django.contrib import admin

# Register your models here.
from .models import *

# 分类展示


class Topiclist(admin.ModelAdmin):
    list_display = ['id', 'name']  # 分类
    list_editable = ['name']  # 可编辑项


class Postlist(admin.ModelAdmin):
    ordering = ['-ctime']  # 文章排序
    list_display = ['title', 'topic', 'ctime']  # 分类
    # list_editable = ['title']  # 可编辑项
    fields = (('title', 'topic'), 'body', 'ctime', 'visiting',
              'parent', 'prev_post', 'level')  # 指定文章发布选项

    list_per_page = 100  # 每页显示条数

    search_fields = ['title']  # display 展示表字段，filter过滤分类，search搜索内容
    date_hierarchy = 'ctime'  # 按时间分类


admin.site.register(Topic, Topiclist)
admin.site.register(Post, Postlist)

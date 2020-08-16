from django.contrib import admin
from  .models import *



@admin.register(Post)
class Post_list(admin.ModelAdmin):
    ordering = ['-id']  # 文章排序
    list_display = ['title','topics','gmt_create']  # 分类
    list_filter = ['gmt_create', 'topics']
    # list_editable = ['title']  # 可编辑项
    fields = (('title', 'topics'),'body','gmt_create','visiting','parent','prev_post','level')  # 指定文章发布选项

    list_per_page = 100 #每页显示条数

    search_fields = ['title']   #display 展示表字段，filter过滤分类，search搜索内容
    date_hierarchy = 'gmt_create' #按时间分类
@admin.register(Topic)
class Topic_list(admin.ModelAdmin):
    list_display = ['name','index','get_items']
    list_editable = ['index']
    readonly_fields = ('get_items',)  


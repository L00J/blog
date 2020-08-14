from django.utils.text import capfirst
from django.contrib import admin

from .models import Article, Category, Tag


# 列表
class Articleslist(admin.ModelAdmin):

    def get_queryset(self, request):
        """函数作用：使当前登录用户只能看到自己所属内容"""
        qs = super(Articleslist, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    ordering = ['-mod_date']
    list_display = ['title', 'category', 'mod_date', 'author']  # 分类
    list_filter = ['publish', 'category']  # 右侧过滤栏
    # list_editable = ['category'] #可编辑项

    empty_value_display = '无数据'  # 空数据
    # fk_fields = ('tags',) # 设置显示外键字段

    list_per_page = 100  # 每页显示条数

    search_fields = ['title']  # display 展示表字段，filter过滤分类，search搜索内容
    date_hierarchy = 'mod_date'  # 按时间分类

    # exclude = ('view','comment','publish') # 排除字段
    fields = (('title', 'category'), 'body', ('tags', 'status'),
              ('picture', 'publish'))  # 指定文章发布选项

    # 重写ModelAdmin模块的save_model方法
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user.username
        obj.save()


# 分类展示
class Categoryslist(admin.ModelAdmin):
    list_display = ['id', 'name']  # 分类
    list_editable = ['name']  # 可编辑项


# 分类排序


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        for app in templateresponse.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse

    return inner


admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)


admin.site.register(Article, Articleslist)
admin.site.register(Category, Categoryslist)
admin.site.register(Tag)


admin.site.site_header = '网站管理系统'
admin.site.site_title = '以谁为师博客'

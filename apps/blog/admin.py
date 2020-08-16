from django.utils.text import capfirst
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.forms import TextInput, Textarea
# from django.db import models
from .models import *


@admin.register(Article)
class Articles_list(admin.ModelAdmin):
    def get_queryset(self, request):
        """函数作用：使当前登录用户只能看到自己所属内容"""
        qs = super(Articles_list, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    ordering = ['-gmt_modified']
    list_display = ['title', 'category',  'cover_data','access_permissions','comment_permissions','localized_img','is_recommend','gmt_modified','author']  # 分类
    list_filter = ['gmt_create', 'category','tags']  # 右侧过滤栏
    list_editable = ('category','access_permissions','comment_permissions','localized_img', 'is_recommend')
    readonly_fields = ('cover_admin', )
    empty_value_display = '无数据'  # 空数据
    fk_fields = ('tags',) # 设置显示外键字段
    list_per_page = 50  # 每页显示条数

    search_fields = ['title']  # display 展示表字段，filter过滤分类，search搜索内容
    date_hierarchy = 'gmt_create'  # 按时间分类

    # exclude = ('view','comment','publish') # 排除字段
    fields = (('title', 'category'), 'body', ('tags', 'status'),
              ( 'gmt_create','cover','access_permissions','comment_permissions','localized_img','is_recommend'))  # 指定文章发布选项

    # 重写ModelAdmin模块的save_model方法
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user.username
        obj.save()

@admin.register(Category)
class Categorys_list(admin.ModelAdmin):
    """
    分类
    """
    list_display = ['name','index','get_items','active','icon','icon_data']  
    list_editable = ['index','active','icon']
    readonly_fields = ('get_items',)  

admin.site.register(Tag) # 标签




@admin.register(FriendLink)
class LinksAdmin(ImportExportModelAdmin):
    """
    友链
    """
    list_display = ('title', 'url', 'avatar_data', 'desc',)
    search_fields = ('title', 'url', 'desc')
    readonly_fields = ('avatar_admin', )
    list_editable = ('url',)

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'desc', 'avatar_admin', 'image', )
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '59'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 59})},
    }


@admin.register(Carousel)
class Carousel_list(admin.ModelAdmin):
    """
    幻灯
    """
    list_display = ['number', 'title','img_url']  
    list_editable = ['img_url']  

# 排序
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


# admin.site.register(Article, Articleslist)
# admin.site.register(Category, _)






admin.site.site_header = '网站管理系统'
admin.site.site_title = '以谁为师博客'

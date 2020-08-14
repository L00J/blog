# Create your views here.
from django.shortcuts import render, get_object_or_404
from blog.models import Article, Category, Tag
from topic.models import *

import markdown
from django.views.generic import ListView  # DetailView
from django.utils.safestring import mark_safe

from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 分页模块


from django.views import View

from django.contrib.auth.decorators import login_required

from haystack.generic_views import SearchView


# @login_required
def index(request):
    """
    博客首页
    :param request:
    :return:
    """
    post_all = Article.objects.order_by('-status', '-publish')  # 博客所有

    topic_indexes = {}
    topic_all = Topic.objects.all()  # 专题
    for t in topic_all:
        k = [i.pk for i in Post.objects.filter(topic=t.pk)[:1]]
        if len(k) > 0:
            topic_indexes[k[0]] = t.name

    page = Paginator(post_all, 5)  # 将文章数分页(2)

    page_num = page.num_pages  # 分页数总数
    page_range = page.page_range  # 页码的列表数目

    page_first = page.page(1)  # 第1页的page对象
    # page_first_list = page_first.object_list  # 首页展示文章条数

    page_count = page.count  # 总数据量

    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取page的值，url内输入的?page = 页码数  显示你输入的页面数目 默认为第1页
        num = request.GET.get('page', 1)
        # 获取第几页
        number = page.page(1)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = page.page(1)
    except EmptyPage:
        number = page.page(page.num_pages)

    start = int(num)  # 当前页面数

    if page_num > 5:  # 总分页数大于5
        if start + 5 > page_num:  # 你输入的值
            pageRange = range(start - 4, start + 1)  # 大于展示按钮数量时

        else:
            pageRange = range(start, start + 5)  # 显示分页按钮数量

    else:
        pageRange = page.page_range  # 正常分配range(1, 4)

    currentPage = page.page(num)  # 当前页面

    currentRange = currentPage.number + 1  # 显示末尾

    article_list = currentPage.object_list

    tag_all = [tag for tag in Tag.objects.all()]  # tags

    if request.user.is_authenticated:  # 登录
        user_login = True

    return render(request, 'index.html', locals())


# # from haystack.views import SearchView
# class MySeachView(SearchView):
#
#
#     def extra_context(self):       #重载extra_context来添加额外的context内容
#         context = super(MySeachView,self).extra_context()
#
#         tag_all = [tag for tag in Tag.objects.all()]  # tags
#
#         context = locals()
#         return context


# class IndexView(View):
#     """
#     cbv 基于类视图
#     """
#     def get(self, request):
#
#         post_all = Article.objects.order_by('-status','-publish')# 博客所有
#
#
#         topic_indexes = {}
#         topic_all = Topic.objects.all() # 专题
#         for t in topic_all:
#             k = [i.pk for i in Post.objects.filter(topic=t.pk)[:1]]
#             if len(k) >0:
#                 topic_indexes[k[0]] = t.name
#
#
#         page = Paginator(post_all, 5)  # 将文章数分页(2)
#
#         page_num = page.num_pages  # 分页数总数
#         page_range = page.page_range  # 页码的列表数目
#
#         page_first = page.page(1)  # 第1页的page对象
#         # page_first_list = page_first.object_list  # 首页展示文章条数
#
#
#         page_count = page.count  # 总数据量
#
#         try:
#             # GET请求方式，get()获取指定Key值所对应的value值
#             # 获取page的值，url内输入的?page = 页码数  显示你输入的页面数目 默认为第1页
#             num = request.GET.get('page', 1)
#             # 获取第几页
#             number = page.page(1)
#         except PageNotAnInteger:
#             # 如果输入的页码数不是整数，那么显示第一页数据
#             number = page.page(1)
#         except EmptyPage:
#             number = page.page(page.num_pages)
#
#         start = int(num)  # 当前页面数
#
#         if page_num   > 5: # 总分页数大于5
#             if start +5 > page_num:  # 你输入的值
#                 pageRange = range(start-4, start+1) # 大于展示按钮数量时
#
#             else:
#                 pageRange = range(start, start+5)  # 显示分页按钮数量
#
#         else:
#             pageRange = page.page_range # 正常分配range(1, 4)
#
#
#         currentPage = page.page(num)  # 当前页面
#
#         currentRange = currentPage.number+1 # 显示末尾
#
#
#
#         article_list = currentPage.object_list
#
#         tag_all = [tag for tag in Tag.objects.all()]  # tags
#
#         if request.user.is_authenticated:  # 登录
#             user_login = True
#
#         return render(request, 'index.html', locals())
#


@login_required
def category(request, pk):
    # 记得在开始部分导入 Category 类

    topic_indexes = {}
    topic_all = Topic.objects.all()  # 专题
    for t in topic_all:
        k = [i.pk for i in Post.objects.filter(topic=t.pk)[:1]]
        if len(k) > 0:
            topic_indexes[k[0]] = t.name

    if request.user.is_authenticated:
        user_login = True

    tag_all = [tag for tag in Tag.objects.all()]

    cate = get_object_or_404(Category, pk=pk)
    post_all = Article.objects.filter(category=cate).order_by('-publish')

    page = Paginator(post_all, 9)  # 将文章数分页(2)

    page_num = page.num_pages  # 分页数总数
    page_range = page.page_range  # 页码的列表数目

    page_first = page.page(1)  # 第1页的page对象
    # page_first_list = page_first.object_list  # 首页展示文章条数

    page_count = page.count  # 总数据量

    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取page的值，url内输入的?page = 页码数  显示你输入的页面数目 默认为第1页
        num = request.GET.get('page', 1)
        # 获取第几页
        number = page.page(1)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = page.page(1)
    except EmptyPage:
        number = page.page(page.num_pages)

    start = int(num)  # 当前页面数

    if page_num > 5:  # 总分页数大于5
        if start + 5 > page_num:  # 你输入的值
            pageRange = range(start - 5, start)

        else:
            pageRange = range(start, start + 5)  # 显示分页按钮数量

    else:
        pageRange = page.page_range  # 正常分配range(1, 4)

    currentPage = page.page(num)  # 当前页面
    article_list = currentPage.object_list

    return render(request, 'blog/category.html', context=locals())


# @login_required
def tag(request, name):
    """
    标签
    :param request:
    :param name
    :return:
    """
    tag_all = [tag for tag in Tag.objects.all()]
    article_list = Article.objects.filter(tags__name=name)
    return render(request, 'index.html', {"article_list": article_list,
                                          "tag_all": tag_all
                                          })


def detail(request, pk):
    """
    博文详情
    """
    topic_indexes = {}
    topic_all = Topic.objects.all()  # 专题
    for t in topic_all:
        k = [i.pk for i in Post.objects.filter(topic=t.pk)[:1]]
        if len(k) > 0:
            topic_indexes[k[0]] = t.name

    ua = request.META.get('HTTP_USER_AGENT')
    ipaddr = request.META['REMOTE_ADDR']

    article = get_object_or_404(Article, pk=pk)
    article.viewed()  # 阅读量统计
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    article.body = md.convert(article.body.replace("\r\n", '\n'))
    toc = md.toc

    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = article.comment_set.all()

    detail_tag = Article.objects.get(pk=pk).tags.all()

    if request.user.is_authenticated:
        user_login = True

    # context = {"article": article,
    #            'form': form,
    #            "ua":ua,
    #            "ipaddr":ipaddr,
    #            'comment_list': comment_list,
    #            "source_id": article.id,
    #            'toc': md.toc }

    context = locals()
    return render(request, 'blog/detail.html', context)

#
# def articles(request, pk):
#     """
#     博客列表页面
#     :param request:
#     :param pk:
#     :return:
#     """
#     pk = int(pk)
#     if pk:
#         category_object = get_object_or_404(Category, pk=pk)
#         category = category_object.name
#         article_list = Article.objects.filter(category_id=pk)
#     else:
#         # pk为0时表示全部
#         article_list = Article.objects.all()  # 获取全部文章
#         category = ''
#     return render(request, 'blog/articles.html', {"article_list": article_list,
#                                                   "category": category,
#                                                   })


def archive(request, year, month):
    """
    归档
    :param request:
    :param year:
    :param month:
    :return:
    """
    article_list = Article.objects.filter(
        publish__year=year, publish__month=month).order_by('-publish')
    return render(request, 'blog/archive.html', context={"article_list": article_list})


class TagView(View):
    model = Tag
    context_object_name = 'tags'
    template_name = 'blog/tags.html'


class CategoryView(View):
    model = Category
    context_object_name = 'categories'
    template_name = 'blog/category.html'


class ArchiveView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'blog/archive.html'


class MySearchView(SearchView):
    """My custom search view."""

    # def get_queryset(self):
    #     queryset = super(MySearchView, self).get_queryset()
    #     # further filter queryset based on some set of criteria
    #     return queryset.filter(pub_date__gte=date(2015, 1, 1))

    def get_context_data(self, *args, **kwargs):

        context = super(MySearchView, self).get_context_data(*args, **kwargs)

        tag_all = [tag for tag in Tag.objects.all()]

        # do something

        topic_indexes = {}
        topic_all = Topic.objects.all()  # 专题
        for t in topic_all:
            k = [i.pk for i in Post.objects.filter(topic=t.pk)[:1]]
            if len(k) > 0:
                topic_indexes[k[0]] = t.name

        context = locals()
        return context


def search(request):
    """
    搜索页面
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        user_login = True

    topic_indexes = {}
    topic_all = Topic.objects.all()  # 专题
    for t in topic_all:
        k = [i.pk for i in Post.objects.filter(topic=t.pk)[:1]]
        if len(k) > 0:
            topic_indexes[k[0]] = t.name

    key = request.GET.get('key')
    error_msg = ''

    tag_all = [tag for tag in Tag.objects.all()]

    if not key:
        error_msg = "请输入关键词"
        return render(request, 'index.html', {'error_msg': error_msg})

    elif request.user.is_authenticated:  # 判断是否登录
        article_list = Article.objects.filter(title__icontains=key)
        return render(request, 'index.html', {'error_msg': error_msg,
                                              "tag_all": tag_all,
                                              "user_login": user_login,
                                              "article_list": article_list, "key": key})
    else:
        error_msg = mark_safe('''<div class="alert alert-info">
				 <button type="button" class="close" data-dismiss="alert">×</button>
				<h4>
					提示!
				</h4> <strong>搜索失败!</strong> 请先登录 ...
			</div>''')
        return render(request, 'index.html', {'error_msg': error_msg})

    # article_list = Article.objects.filter(Q(title__icontains=key) | Q(body__icontains=key))
    # 全文搜索

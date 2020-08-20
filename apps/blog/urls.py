#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------
# Author:    LJ
# Email:     admin@attacker.club

# Date:      18-5-29
# Description:
# --------------------------------------------------


from django.urls import path, re_path, include
# re_path方法相当于 django1.11 url正则表达式
from .views import *
# 载入视图模块

# from haystack.views import SearchView

app_name = 'blog'
# 设置应用命名空间

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # 主页，自然排序
    path('hot/', IndexView.as_view(), {'sort': 'v'}, name='index_hot'),  # 主页，按照浏览量排序
    path('article/<slug:slug>/', DetailView.as_view(), name='detail'),  # 文章内容页
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('category/<slug:slug>/hot/', CategoryView.as_view(), {'sort': 'v'},
        name='category_hot'),
    path('tag/<slug:slug>/', TagView.as_view(), name='tag'),
    path('tag/<slug:slug>/hot/', TagView.as_view(), {'sort': 'v'}, name='tag_hot'),
    path('about/', AboutView, name='about'),  # About页面
    path('archive/', ArchiveView.as_view(), name='archive'),  # 归档页面
    path('search/', MySearchView.as_view(), name='search_view'),  # 全文搜索
    # path('timeline/', TimelineView.as_view(), name='timeline'),  # timeline页面
    # path('silian.xml', SilianView.as_view(content_type='application/xml'), name='silian'),  # 死链页面

    # path('', views.IndexView.as_view(), name="index"),
    # r正则;（）取出的内容;?P<> 里面是视图的参数名;[0-9]+数字;$结尾
    # re_path(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # re_path(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # re_path(r'^detail/(?P<pk>\d+)/$', views.detail, name='detail'),
    #re_path(r'^detail/(?P<pk>\d+).html$', views.detail, name='detail'),
    # re_path(r'^archive/$', views.archive, name='archive'),
    #re_path(r'^articles/$', views.archive, name='articles'),
    # re_path(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archive, name='archive'),
  
]

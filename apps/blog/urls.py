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

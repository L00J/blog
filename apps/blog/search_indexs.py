#!/usr/bin/env python
# coding=utf-8
'''
Author: 以谁为师
Website: attacker.club
Date: 2020-08-20 00:19:05
LastEditTime: 2020-08-20 00:19:09
Description: 
'''
# -*- coding: utf-8 -*-

from haystack import indexes
from .models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    views = indexes.IntegerField(model_attr='views')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

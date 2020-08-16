from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from mdeditor.fields import MDTextField


class Topic(models.Model):
    name = models.CharField(max_length=128, verbose_name="主题")
    index = models.IntegerField(default=99, verbose_name='排序')

    # 统计文章数 并放入后台
    def get_items(self):
        return self.post_set.all().count()
    get_items.short_description = '文章数'
    def __str__(self):
        return self.name

    class Meta:
        db_table = "wy_tutorial_topic"
        verbose_name = "主题"
        verbose_name_plural = verbose_name



class Post(models.Model):
    title = models.CharField(max_length=128, verbose_name="文章")
    body = MDTextField(verbose_name='正文', blank=True, null=True)
    #body = models.TextField(verbose_name="正文")
    topics = models.ForeignKey("Topic",  on_delete=models.CASCADE,verbose_name="所属专题")
    visiting = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="访问量")
    parent = models.ForeignKey("self", blank=True, default=None, null=True, related_name="child_post", on_delete=models.CASCADE,                              verbose_name="父亲文章")
    prev_post = models.OneToOneField("self", default=None, blank=True, null=True, related_name="next_post",
                                     on_delete=models.CASCADE,verbose_name="前一篇文章")
    gmt_create = models.DateTimeField(verbose_name='发布时间', default=timezone.now)  # 发布时间
    # ctime = models.DateTimeField(auto_now_add=True)
    gmt_modified = models.DateTimeField(auto_now=True)
    level = models.PositiveSmallIntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return self.topic.name + "......" + self.title

    def increase_views(self):
        self.visiting += 1
        self.save(update_fields=['visiting'])

    def save(self, *args, **kwargs):

        if not self.parent:
            self.level = 0
        else:
            self.level = self.parent.level + 1
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'Topic':self.Topic.name,'post_id': self.id})

    class Meta:
        db_table = "wy_tutorial_post"
        verbose_name = "内容"
        verbose_name_plural = verbose_name
        ordering = ["gmt_create"]
from django.db import models
from django.utils import timezone

from mdeditor.fields import MDTextField


class Category(models.Model):  # 分类
    """
    继承django.db.models.Models模块
    """
    name = models.CharField(verbose_name='文章分类', max_length=100)

    class Meta:
        verbose_name_plural = "分类"

    def __str__(self):
        return self.name


class Tag(models.Model):  # 标签
    name = models.CharField(verbose_name='标签', max_length=100)

    class Meta:
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    django会自动新建自增id作为主键
    """

    status_choice = (
        (0, '原'),
        (1, '转'),
        (2, '顶'),
    )

    title = models.CharField(verbose_name='标题', max_length=70)  # 标题
    body = MDTextField(verbose_name='正文', blank=True, null=True)
    # body = models.TextField(verbose_name='正文',blank=True, null=True)  # 文章正文
    digest = models.TextField(blank=True, null=True)  # 文章摘要
    status = models.SmallIntegerField(
        choices=status_choice, default=0, verbose_name='类型')
    publish = models.DateTimeField(
        verbose_name='发布时间', default=timezone.now)  # 发布时间
    mod_date = models.DateField(verbose_name='更新时间', auto_now=True)  # 更新时间

    category = models.ForeignKey(
        Category, verbose_name='分类', on_delete=models.CASCADE)
    # 分类
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)  # 标签

    view = models.BigIntegerField(verbose_name='阅读数', default=0)  # 阅读数
    # comment = models.BigIntegerField(verbose_name='评论数',default=0)  # 评论数
    author = models.CharField(
        default='anonymous', verbose_name='作者', editable=False, max_length=128)
    picture = models.CharField(
        verbose_name='图片地址', max_length=200, blank=True, null=True)  # 图片地址

    def __str__(self):
        return self.title

    def viewed(self):
        """
        增加阅读数
        :return:
        """
        self.view += 1
        self.save(update_fields=['view'])
    # def commenced(self):
    #     """
    #     增加评论数
    #     :return:
    #     """
    #     self.comment += 1
    #     self.save(update_fields=['comment'])

    def save(self, *args, **kwargs):
        """
        重写摘要
        :param args:
        :param kwargs:
        :return:
        """
        body = self.body

        # 从 body 摘取前 54 个字符赋给到 excerpt
        self.digest = body[:80]
        # 调用父类的 save 方法将数据保存到数据库中
        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-publish']
        verbose_name_plural = "文章"


#
# class Comment(models.Model):
#     title = models.CharField("标题", max_length=100)
#     source_id = models.CharField('文章id或source名称', max_length=25)
#     create_time = models.DateTimeField('评论时间', auto_now=True)
#     user_name = models.CharField('评论用户', max_length=25)
#     url = models.CharField('链接', max_length=100)
#     comment = models.CharField('评论内容', max_length=500)


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name

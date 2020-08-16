from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField 
from django.utils.html import format_html 
from django.shortcuts import reverse 

class Tag(models.Model):  
    """
    文章标签
    """
    name = models.CharField(max_length=30,verbose_name='标签名称')

    # 统计文章数 并放入后台
    def get_items(self):
        return self.article_set.all().count()
    get_items.short_description = '文章数'

    class Meta:
        db_table = "wy_blog_tag"
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):  
    """
    文章分类
    """
    id = models.AutoField(primary_key=True, verbose_name="编号")
    name = models.CharField(max_length=30,verbose_name='分类名称')
    index = models.IntegerField(default=99, verbose_name='分类排序')
    active = models.BooleanField(default=False, verbose_name='是否添加到菜单')
    icon = models.CharField(max_length=30, default='fa fa-home', verbose_name='菜单图标')

    # 统计文章数 并放入后台
    def get_items(self):
        return self.article_set.all().count()
    get_items.short_description = '文章数'

    def icon_data(self):
        return format_html(
            '<i class="{}"></i>',
            self.icon,
        )
    icon_data.short_description = '图标预览'

    class Meta:
        db_table = "wy_blog_category"
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
      

class Article(models.Model):
    """
    文章
    """

    status_choice = (
        (0, '原创'),
        (1, '转发'),
        (2, '关注'),
    )

    title = models.CharField(verbose_name='标题', max_length=70)  # 标题
    body = MDTextField(verbose_name='正文', blank=True, null=True)
    # body = models.TextField(verbose_name='正文',blank=True, null=True)  # 文章正文
    digest = models.TextField(blank=True, null=True)  # 文章摘要
    
    gmt_create = models.DateTimeField(
        verbose_name='发布时间', default=timezone.now)  # 发布时间
    gmt_modified = models.DateField(verbose_name='更新时间', auto_now=True)  # 更新时间

    category = models.ForeignKey(
        Category, verbose_name='分类', on_delete=models.CASCADE)
    # 分类
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)  # 文章标签

    view = models.BigIntegerField(verbose_name='阅读数', default=0)  # 阅读数
    # comment = models.BigIntegerField(verbose_name='评论数',default=0)  # 评论数
    author = models.CharField(
        default='anonymous', verbose_name='作者', editable=False, max_length=128)
    # picture = models.CharField(
    #     verbose_name='图片地址', max_length=200, blank=True, null=True)  # 图片地址
    cover = models.CharField(max_length=200, default='/static/default/code.jpg', verbose_name='文章封面')
    status = models.SmallIntegerField(
        choices=status_choice, default=0, verbose_name='类型')
    access_permissions = models.BooleanField(default=False, verbose_name='仅自己可见')
    comment_permissions = models.BooleanField(default=False, verbose_name='禁止评论')
    localized_img = models.BooleanField(default=False, verbose_name='下载外站图片到本地')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')


    def cover_data(self):
        return format_html(
            '<img src="{}" width="156px" height="98px"/>',
            self.cover,
        )

    def cover_admin(self):
        return format_html(
            '<img src="{}" width="440px" height="275px"/>',
            self.cover,
        )
    cover_data.short_description = '文章封面'
    cover_admin.short_description = '文章封面'



    def __str__(self):
        return self.title

    def viewed(self):
        """
        增加阅读数
        :return:
        """
        self.view += 1
        self.save(update_fields=['view'])



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
        db_table = "wy_blog_article"
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-gmt_create']



class Author(models.Model):
    """
    作者
    """
    name = models.CharField(max_length=50)
    email = models.EmailField()   


    class Meta:
        db_table = "wy_blog_author"
        verbose_name = "文章作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name




# 幻灯片
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField('标题', max_length=20, blank=True, null=True, help_text='标题可以为空')
    content = models.CharField('描述', max_length=80)
    img_url = models.CharField('图片地址', max_length=200)
    url = models.CharField('跳转链接', max_length=200, default='#', help_text='图片跳转的超链接，默认#表示不跳转')
   

    class Meta:
        db_table = "wy_blog_carousel"
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]




class FriendLink(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    url = models.URLField(verbose_name='地址')
    desc = models.TextField(verbose_name='描述', max_length=250)
    image = models.URLField(default='https://image.3001.net/images/20190330/1553875722169.jpg', verbose_name='头像')

    def avatar_data(self):
        return format_html(
            '<img src="{}" width="50px" height="50px" style="border-radius: 50%;" />',
            self.image,
        )

    def avatar_admin(self):
        return format_html(
            '<img src="{}" width="250px" height="250px"/>',
            self.image,
        )

    avatar_data.short_description = '头像'
    avatar_admin.short_description = '头像预览'
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    # is_active = models.BooleanField('是否有效', default=True)
    # is_show = models.BooleanField('是否首页展示', default=False)

    class Meta:
        db_table = "wy_blog_friendlink"
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.title

    def get_home_url(self):
        '''提取友链的主页'''
        u = re.findall(r'(http|https://.*?)/.*?', self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=['is_show'])


class About(models.Model):
    body = models.TextField(verbose_name='About 内容')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = "wy_blog_About"
        verbose_name = 'About'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'About'

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])



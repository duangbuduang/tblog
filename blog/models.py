import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags


class Category(models.Model):
    """文章分类"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Post(models.Model):
    """文章"""
    # 文章标题
    title = models.CharField('标题', max_length=70)
    # 正文
    body = models.TextField('正文')
    # 创建时间
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    # 修改时间
    modified_time = models.DateTimeField('修改时间')
    # 摘要
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 分类  ForeignKey 必须传入一个 on_delete 参数用来指定当关联的数据被删除时，被关联的数据的行为
    #  models.CASCADE 参数，意为级联删除
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    # 标签
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 文章作者 这里 User 是从 django.contrib.auth.models 导入的
    # django.contrib.auth是django内置的应用，专门用于处理网站用户的注册、登录等流程，User是django为我们已经写好的用户模型
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']  # 指定排序方式

    def save(self, *args, **kwargs):
        """重写父类方法save,每次保存前修改下修改时间"""
        self.modified_time = timezone.now()
        # 实例化一个Markdown类，用于渲染body的文本
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """获取url"""
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        """更新阅读量"""
        self.views += 1
        self.save(update_fields=['views'])

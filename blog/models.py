from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """文章分类"""
    name = models.CharField(max_length=100)


class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=100)


class Post(models.Model):
    """文章"""
    # 文章标题
    title = models.CharField(max_length=70)
    # 正文
    body = models.TextField()
    # 创建时间
    created_time = models.DateTimeField()
    # 修改时间
    modified_time = models.DateTimeField()
    # 摘要
    excerpt = models.CharField(max_length=200, blank=True)

    # 分类  ForeignKey 必须传入一个 on_delete 参数用来指定当关联的数据被删除时，被关联的数据的行为
    #  models.CASCADE 参数，意为级联删除
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 标签
    tag = models.ManyToManyField(Tag, blank=True)

    # 文章作者 这里 User 是从 django.contrib.auth.models 导入的
    # django.contrib.auth是django内置的应用，专门用于处理网站用户的注册、登录等流程，User是django为我们已经写好的用户模型
    author = models.ForeignKey(User, on_delete=models.CASCADE)


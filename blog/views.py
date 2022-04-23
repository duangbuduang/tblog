import re

import markdown
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension

from blog.models import Post, Category, Tag


# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(ListView):
    """（首页）所有文章类视图"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


def login(request):
    return render(request, 'blog/login.html')


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',  # 自动生成目录的拓展
#                                   ])
#     return render(request, 'blog/detail.html', context={'post': post})


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views()  # 阅读量+1
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#         # TocExtension(slugify=slugify)
#     ])
#     post.body = md.convert(post.body)
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#
#     return render(request, 'blog/detail.html', context={'post': post})


class PostDetailView(DetailView):
    """文章详情"""
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post


# def archive(request, year, month):
#     """归档"""
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list
#     })


class ArchiveView(ListView):
    """归档"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


# def category(request, pk):
#     """分类"""
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list
#     })


class CategoryView(ListView):
    """分类"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# def tag(request, pk):
#     """标签"""
#     t = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=t)
#     return render(request, 'blog/index.html', context={
#         'post_list': post_list
#     })


class TagView(ListView):
    """标签"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)

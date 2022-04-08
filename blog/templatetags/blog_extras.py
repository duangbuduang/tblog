"""自定义模板标签"""

from django import template

from blog.models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    """最新文章"""
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[: num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    """归档"""
    # 这里 Post.objects.dates 方法会返回一个列表
    # 列表中的元素为每一篇文章（Post）的创建时间（已去重），且是 Python 的 date 对象，精确到月份，降序排列。
    # 接受的三个参数值表明了这些含义，一个是 created_time ，即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）。
    # 例如我们写了 3 篇文章，分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，
    # 那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    """分类"""
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    """标签云"""
    return {
        'tag_list': Tag.objects.all(),
    }

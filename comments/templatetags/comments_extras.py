from django import template

from comments.forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    """表单"""
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    # post.comment_set.all() 来获取 post 对应的全部评论
    # post.comment_set.all() 也等价于 Comment.objects.filter(post=post)
    # 例如 Post.objects.filter(category=cate) 也可以等价写为 cate.post_set.all()
    comment_list = post.comment_set.all()
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from blog.models import Post
from comments.forms import CommentForm


@require_POST
def comment(request, post_pk):
    """
    评论
    :param request:
    :param post_pk: 被评论的文章
    :return:
    """
    # 先获取被评论的文章，因为后面要把评论和被评论的文章关联起来
    post = get_object_or_404(Post, pk=post_pk)
    # django将用户提交的数据封装在了request.POST里，这是一个类字典对象
    # 我们利用这些数据构造了CommentForm的实例，这样就生成了一个绑定用户提交数据的表单
    form = CommentForm(request.POST)

    # 调用is_valid()方法让django自动帮我们检查表单的数据是否符合格式要求
    if form.is_valid():
        # 表单合法时，调用表单的save方法保存数据到数据库，commit=False的作用：仅利用表单数据生成Comment模型类的实例，但还不保存到数据库
        comment = form.save(commit=False)
        # 将评论和被评论的文章关联起来
        comment.post = post
        # 将评论数据保存到数据库，调用模型实例的save方法
        comment.save()

        # 使用 add_message 方法增加了一条消息
        # 发送的消息被缓存在 cookie 中，然后我们在模板中获取显示即可
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        # 重定向到post（文章）的详情页，当redirect函数接收一个模型的实例时，它会调用这个模型实例的get_absolute_url方法，
        return redirect(post)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
    context = {
        'post': post,
        'form': form,
    }

    # 使用 add_message 方法增加了一条消息
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)

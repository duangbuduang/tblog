from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment  # 表明这个表单对应的数据库模型是 Comment 类
        fields = ['name', 'email', 'url', 'text']  # 指定了表单需要显示的字段

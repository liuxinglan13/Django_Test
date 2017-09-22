from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
register = template.Library()


# 已发布的帖子的总数
@register.simple_tag
def total_posts():
    return Post.published.count()


# 最新发布的帖子（count 参数 显示 几条 默认5） 渲染 latest_post.html 模版
@register.inclusion_tag('app/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# 查询出评论最多的5条博客
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                total_comments=Count('comments')
            ).order_by('-total_comments')[:count]


# 自定义的markdown过滤器
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))



import django_filters

from guild.models import Response, Post


class ResponseFilter(django_filters.FilterSet):
    class Meta:
        model = Response
        fields = ['created_at', 'is_approved']


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'category', 'created_at', 'content']

import django_filters
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from guild.models import Response, Post


# class ResponseFilter(django_filters.FilterSet):
#     class Meta:
#         model = Response
#         fields = ['created_at', 'is_approved']


class ResponseFilter(FilterSet):
    category = CharFilter(field_name='post__category__name', lookup_expr='icontains')


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'category', 'created_at', 'content']

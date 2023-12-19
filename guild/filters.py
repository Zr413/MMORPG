from django.forms import DateInput
from django_filters import CharFilter, DateFilter, ModelChoiceFilter
from django_filters.rest_framework import FilterSet

from guild.models import Post, Category


class ResponseFilter(FilterSet):
    category = CharFilter(field_name='post__category__name', lookup_expr='icontains')


class PostFilter(FilterSet):
    created_at = DateFilter(
        field_name="created_at",
        lookup_expr='icontains',
        widget=DateInput(format='%Y-%m-%d',
                         attrs={'type': 'date'}, ))
    category = ModelChoiceFilter(field_name="category", queryset=Category.objects.all(), label='Категория')
    content = CharFilter(field_name="content", lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['category', 'created_at', 'content']

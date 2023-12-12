from django.contrib import admin
from .models import Post, Profile, Response, Category, Subscription

from modeltranslation.admin import \
    TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


# Register your models here.

# Регистрируем модели для перевода в админке

class CategoryAdmin(TranslationAdmin):
    model = Category


class NewsAdmin(TranslationAdmin):
    model = Post


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Response)
admin.site.register(Subscription)

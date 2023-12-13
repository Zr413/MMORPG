import django_filters
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django_filters.views import FilterView

from .forms import ProfileForm, PostForm
from .models import Post, Response, Profile, Category, Subscription
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator

import pytz

from django.contrib import messages
from .forms import UserRegisterForm
from .filters import ResponseFilter, PostFilter


# Показать все объявления
class PostListView(ListView, FilterView):
    model = Post
    ordering = '-created_at'
    context_object_name = 'posts'
    template_name = 'post_list.html'
    paginate_by = 10  # Количество объявлений на странице
    filterset_class = PostFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)
        context['posts'] = posts
        return context


# Показать объявление
class PostDetailView(DetailView):
    model = Post
    form_class = PostForm
    context_object_name = 'post'
    template_name = 'post_detail.html'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта

        obj = cache.get(f'post_{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post_{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# Создать объявление
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('guild.add_post',)
    raise_exception = True
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user=self.request.user)
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']
        return super().form_valid(form) and HttpResponseRedirect('/')

    # Создать объявление
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Обновить объявление
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = ('guild.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']
        return super().form_valid(form) and HttpResponseRedirect('/')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


# Удалить объявление
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/'
    template_name = 'post_delete.html'
    permission_required = ('guild.delete_post',)
    success_url = reverse_lazy('post-list')

    # Проверка на авторство поста
    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class PostSearchView(FilterView):
    model = Post
    template_name = 'post_search.html'
    filterset_class = PostFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class ResponseView(ListView):
    model = Response
    context_object_name = 'responses'
    template_name = 'responses/response_list.html'

    def get_queryset(self):
        # Получаем id поста из URL
        post_id = self.kwargs['post_pk']
        # Возвращаем все отзывы для данного поста
        return Response.objects.filter(post__id=post_id, is_approved=True)


# Ответы на объявления
class ResponseModerationView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses/response_moderation.html'
    context_object_name = 'responses'
    filterset_class = ResponseFilter

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form) and HttpResponseRedirect('/')

    def get_queryset(self):
        return Response.objects.filter(post__author=self.request.user.profile, is_approved=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class ResponseApproveView(View):
    model = Response
    context_object_name = 'responses'

    def post(self, request, *args, **kwargs):
        response = get_object_or_404(Response, id=kwargs['pk'])
        if request.user.profile == response.post.author:
            response.is_approved = True
            response.save()
        return redirect('response-moderation')


# Ответить
class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    fields = ['content']
    template_name = 'responses/response_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        response = form.save()
        send_mail(
            'New Response Received',
            f'You have received a new response to your post: {response.post.title}',
            'from@example.com',
            [response.post.author.user.email],
            fail_silently=False,
        )
        return redirect('post-detail', pk=response.post.pk)


class ResponseDeleteView(DeleteView):
    def post(self, request, *args, **kwargs):
        response = get_object_or_404(Response, id=kwargs['pk'])
        if request.user.profile == response.post.author:
            response.delete()
        return redirect('response-moderation')

    # def delete(self, request, *args, **kwargs):
    #     response_id = request.POST.get('pk')
    #     response = get_object_or_404(Response, pk=response_id)
    #     response.delete()
    #     return JsonResponse({"status": "success"})


# Представление профиля
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.profile.pk})

    def form_valid(self, form):
        messages.success(self.request, "The profile was updated successfully.")
        return super(ProfileUpdateView, self).form_valid(form)


# Регистрация
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'profiles/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        # Создание профиля пользователя при регистрации
        Profile.objects.create(user=self.object)
        return valid


# # Подписка
# @login_required
# @csrf_protect
# def subscriptions(request, action=None, pk=None):
#     if action and pk:
#         category = Category.objects.get(id=pk)
#
#         if action == 'subscribe':
#             Subscription.objects.get_or_create(user=request.user, category=category)
#             messages.success(request, f'Вы успешно подписались на категорию {category.title}!')
#         elif action == 'unsubscribe':
#             Subscription.objects.filter(user=request.user, category=category).delete()
#             messages.success(request, f'Вы успешно отписались от категории {category.title}!')
#
#     categories = Category.objects.annotate(
#         user_subscribed=Exists(
#             Subscription.objects.filter(
#                 user=request.user,
#                 category=OuterRef('pk'),
#             )
#         )
#     ).order_by('title')
#
#     return render(request, 'post_subscription.html', {'categories': categories})

class SubscriptionView(View):
    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=kwargs['pk'])
        profile = Profile.objects.get(user=request.user)
        subscription, created = Subscription.objects.get_or_create(profile=profile, category=category)
        if created:
            subscription.subscribed = True
            subscription.save()
            # Отправка письма
            subject = 'Вы успешно подписались!'
            message = f'Вы подписались на категорию {category.name}. Вы можете отписаться, перейдя по ' \
                      f'ссылке: http://{get_current_site(request)}/unsubscribe/{subscription.id}/'
            send_mail(subject, message, 'from@example.com', [request.user.email])
        return redirect('post-list')
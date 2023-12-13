from django.urls import path

from django.conf.urls.static import static
from MMORPG import settings

from guild import views
from django.contrib.auth import views as auth_views

from guild.views import ResponseApproveView, ResponseModerationView, PostListView, PostDetailView, PostCreateView, \
    PostUpdateView, PostDeleteView, ResponseCreateView, ResponseView, PostSearchView, UserRegisterView, \
    ProfileUpdateView, ResponseDeleteView, SubscriptionView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/response/new/', ResponseCreateView.as_view(), name='response-create'),
    path('post/<int:post_pk>/responses/', ResponseView.as_view(), name='response-list'),
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('responses/moderation/', ResponseModerationView.as_view(), name='response-moderation'),
    path('response/<int:pk>/approve/', ResponseApproveView.as_view(), name='response-approve'),
    path('response/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response-delete'),
    path('category/<int:pk>/subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profiles/logout.html'), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

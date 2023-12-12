from django.conf.urls.static import static
from django.urls import path

from MMORPG import settings
from . import views
from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('', views.PostListView.as_view(), name='post-list'),
#     path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
#     path('new/', views.PostCreateView.as_view(), name='post-create'),
#     path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
#     path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
#     path('<int:pk>/response/new/', views.ResponseCreateView.as_view(), name='response-create'),
#     path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
# ]


urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/response/new/', views.ResponseCreateView.as_view(), name='response-create'),
    path('post/<int:post_pk>/responses/', views.ResponseView.as_view(), name='response-list'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profiles/logout.html'), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

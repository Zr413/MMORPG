from django.urls import path

from django.conf.urls.static import static
from MMORPG import settings
from django.contrib.auth import views as auth_views

from guild import views
from guild.views import ResponseApproveView, ResponseModerationView, PostListView, PostDetailView, PostCreateView, \
    PostUpdateView, PostDeleteView, ResponseCreateView, ResponseView, UserRegisterView, \
    ProfileUpdateView, ResponseDeleteView, SubscriptionView, UnsubscribeView, ConfirmRegistrationView, \
    UserPasswordChangeView, UserForgotPasswordView, UserPasswordResetConfirmView

urlpatterns = [
                  path('', PostListView.as_view(), name='post-list'),
                  path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
                  path('post/new/', PostCreateView.as_view(), name='post-create'),
                  path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
                  path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
                  path('post/<int:pk>/response/new/', ResponseCreateView.as_view(), name='response-create'),
                  path('post/<int:post_pk>/responses/', ResponseView.as_view(), name='response-list'),
                  path('responses/moderation/', ResponseModerationView.as_view(), name='response-moderation'),
                  path('response/<int:pk>/approve/', ResponseApproveView.as_view(), name='response-approve'),
                  path('response/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response-delete'),
                  path('category/<int:pk>/subscribe/', SubscriptionView.as_view(), name='subscribe'),
                  path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
                  path('subscriptions/<int:pk>/', UnsubscribeView.as_view(), name='unsubscribe'),
                  path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name='login'),
                  path('сonfirmed/', ConfirmRegistrationView.as_view(), name='confirm'),
                  path('logout/', auth_views.LogoutView.as_view(template_name='profiles/logout.html'), name='logout'),
                  path('register/', UserRegisterView.as_view(), name='register'),
                  path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
                  path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
                  path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
                  path('password-reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='profiles/user_password_reset_done.html'),
                       name='password_reset_done'),
                  path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='profiles/user_password_reset_complete.html'),
                       name='password_reset_complete'),
                  path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('api/post/', views.PostListCreate.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

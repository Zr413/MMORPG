from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver


from MMORPG import settings
from guild.models import Post, Subscription, Response

#  Уведомление автору поста о новом отклике на его пост
@receiver(post_save, sender=Post)
def send_new_post_notification(sender, instance, created, **kwargs):
    if created:
        subscriptions = Subscription.objects.filter(category=instance.category, subscribed=True)
        for subscription in subscriptions:
            subject = 'Новый пост в подписанной категории!'
            message = f'В категории {instance.category.name}, на которую вы подписаны, ' \
                      f'появился новый пост: {instance.title}. Вы можете прочитать его, ' \
                      f'перейдя по ссылке: http://127.0.0.1:8000/post/{instance.id}/'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [subscription.profile.user.email])


# Уведомление автору отклика на пост при обобрении отклика
@receiver(post_save, sender=Response)
def send_approval_notification(sender, instance, created, **kwargs):
    if not created and instance.is_approved:
        post_author = instance.author.user.email  # Получаем автора поста
        subject = 'Ваш отзыв одобрен'
        message = f'Ваш отзыв на пост "{instance.post}" был одобрен.'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [post_author])

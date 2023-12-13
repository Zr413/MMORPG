from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from guild.models import Post, Subscription


@receiver(post_save, sender=Post)
def send_new_post_notification(sender, instance, created, **kwargs):
    if created:
        subscriptions = Subscription.objects.filter(category=instance.category, subscribed=True)
        for subscription in subscriptions:
            subject = 'Новый пост в подписанной категории!'
            message = f'В категории {instance.category.name}, на которую вы подписаны, ' \
                      f'появился новый пост: {instance.title}. Вы можете прочитать его, ' \
                      f'перейдя по ссылке: http://127.0.0.1:8000/post/{instance.id}/'
            send_mail(subject, message, 'from@example.com', [subscription.profile.user.email])

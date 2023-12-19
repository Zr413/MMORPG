from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)
    BIO_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
    ]
    bio = models.CharField(max_length=1, choices=BIO_CHOICES, default='M')
    one_time_password = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.profile

    def check_confirmation_code(self, code):
        return self.one_time_password == code  # Checking if the provided code matches the one in the profile

    def confirm_registration(self):
        self.email_confirmed = True  # Marking the email as confirmed
        self.save()  # Saving the profile


class Category(models.Model):
    name = models.CharField(max_length=100)
    subscribes = models.ManyToManyField(Profile, related_name='categories', through='Subscription')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.title}: {self.content}, {self.title}: {self.category}, {self.title}: {self.image}'

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])


class Response(models.Model):
    post = models.ForeignKey(Post, related_name='responses', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)


class Subscription(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,  related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  related_name='subscriptions')
    subscribed = models.BooleanField(default=False)

    def str(self):
        return f'{self.profile.user.username} subscribed to {self.category.name}'

    class Meta:
        unique_together = ('profile', 'category')
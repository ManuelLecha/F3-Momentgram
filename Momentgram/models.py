from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    web = models.TextField(max_length=500, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_follows")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_is_followed")
    follow_time = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '{} is followed by {}'.format(self.following, self.follower)


class Post(models.Model):
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.description

    class Meta:
        ordering = ('date',)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('date',)

class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_giving_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked")
    date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    comment = models.TextField(max_length=500, blank=True)
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('date',)


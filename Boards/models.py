import math

from django.db import models
from django.contrib.auth.models import User

from django.utils.html import mark_safe
from markdown import markdown


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=30,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255, unique=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    # Foreign Keys
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics',)
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics',)

    def __str__(self):
        return '%s : %s' % (self.board.__str__(), self.subject,)

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 2
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


class Post(models.Model):
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    # Foreign Keys
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts',)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    def __str__(self):
        return '%s : %s' % (self.topic.__str__(), self.message,)

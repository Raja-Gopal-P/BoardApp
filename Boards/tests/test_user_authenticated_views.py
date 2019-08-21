from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ..models import Board
from ..models import Topic
from ..models import Post


class TestLoginRedirection(TestCase):

    def setUp(self):
        self.login_url = reverse('accounts:login')
        self.username = 'john'
        self.password = '123'

        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.board = Board.objects.create(name='Board', description='Description')
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=self.user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=self.user)

    def test_new_topic_unauthenticated_redirection(self):
        url = reverse('Boards:new_topic', kwargs={'pk': self.board.pk})
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=self.login_url,url=url))

    def test_topic_reply_unauthenticated_redirection(self):
        url = reverse('Boards:topic_reply', kwargs={'board_pk': self.board.pk, 'topic_pk': self.topic.pk})
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=self.login_url, url=url))

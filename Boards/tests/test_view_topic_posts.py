from django.test import TestCase
from django.shortcuts import reverse
from django.urls import resolve
from django.contrib.auth.models import User
from ..models import Board
from ..models import Topic
from ..models import Post
from ..views import PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django board.')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        topic = Topic.objects.create(subject='Hello, world', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
        url = reverse('Boards:topic_view', kwargs={'board_pk': board.pk, 'topic_pk': topic.pk})
        self.client.login(username='john', password='123')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)

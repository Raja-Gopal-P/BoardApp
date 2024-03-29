from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.utils import timezone
from django.utils.decorators import method_decorator

from .models import Board
from .models import Topic
from .models import Post
from .forms import NewTopicForm
from .forms import PostForm


class IndexView(ListView):
    model = Board
    template_name = 'Boards/index.html'
    context_object_name = 'boards'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'Boards/topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'Boards/topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('board_pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('Boards:board', pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'Boards/new-topic.html', {'board': board, 'form': form})


@login_required
def topic_reply(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('Boards:topic_view', kwargs={'board_pk': board_pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'Boards/reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class EditPost(UpdateView):

    model = Post
    fields = ('message',)
    template_name = 'Boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()

        return redirect('Boards:topic_view', board_pk=post.topic.board.pk, topic_pk=post.topic.pk)

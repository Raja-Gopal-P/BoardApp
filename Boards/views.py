from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator

from .models import Board
from .models import Topic
from .models import Post
from .forms import NewTopicForm
from .forms import PostForm


# Create your views here.
def index(request):
    boards = Board.objects.all()

    return HttpResponse(render(request, 'Boards/index.html', {'boards': boards}))


def board_page(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'Boards/topics.html', {'board': board, 'topics': topics})


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
def topic_view(request, board_pk, topic_pk):
    topic = get_object_or_404(Topic, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'Boards/topic_posts.html', {'topic': topic})


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
            return redirect('Boards:topic_view', board_pk=board_pk, topic_pk=topic_pk)
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

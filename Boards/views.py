from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Board
from .models import Topic
from .models import Post
from .forms import NewTopicForm


# Create your views here.
def index(request):
    boards = Board.objects.all()

    return HttpResponse(render(request, 'Boards/index.html', {'boards': boards}))


def board_page(request, pk):
    board = get_object_or_404(Board, pk=pk)

    return render(request, 'Boards/topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()

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

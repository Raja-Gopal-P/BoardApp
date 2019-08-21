from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import SignUpForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Boards:index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

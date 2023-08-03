from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
 
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/reg.html'
    success_url = reverse_lazy('login')
    

def post_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_view.html', {'post':post})


def index(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Post.objects.order_by('create_date').order_by('update_date')
    return render(request, 'index.html', {'posts':posts})

        

def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
        return render(request, 'create_post.html', {'form':form})

def post_edit(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.update_date = timezone.now()
            post.author = request.user
            post.save()


        return render(request, 'post_view.html', {'post':post})
    else:
        context = {
            'post': PostForm(instance=post),
            'slug':slug
        }
        return render(request, 'post_edit.html', context)
    
def post_delete(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('home')

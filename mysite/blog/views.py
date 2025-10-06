from .models import Student, Post, Author, Room, Message
from .forms import PostForm
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
from rest_framework import viewsets, filters




@login_required
def Blog_My_Page(request):
    name = request.user.author
    data = Author.objects.prefetch_related('posts').get(author_name = name)
    return render(request, 'blog/blogmypage.html', {'data': data})


def Blog_Author_Page(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        raise PermissionDenied('Tác giả không tồn tại')
    try:
        user = request.user.author
    except Author.DoesNotExist:
        raise PermissionDenied('Bạn chưa có quyền tác giả')
    posts = Post.objects.filter(author=author).order_by('-id')
    show_chat_button = (user != author)
    context = {
        'author': author,
        'posts': posts,
        'user': user,
        'show_chat_button': show_chat_button, 
    }
    return render(request, 'blog/blogauthorpage.html', context)


@login_required
def Post_Update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user.author:
        return PermissionDenied('Không đủ quyền hạn để sửa')
    
    if request.method == 'POST':
        newpost = PostForm(request.POST, request.FILES, instance = post)
        if newpost.is_valid():
            newpost.save()
            return redirect('blogmylist')
    else:
        newpost = PostForm(instance = post)
    
    return render(request, 'blog/postcreate.html', {'form': newpost})


def Blog_Page(request):
    author = []
    posts = Post.objects.all()
    is_title = True
    is_author = False
    if request.method == 'GET':
        input_value =  request.GET.get('data')
        if input_value:
            if Author.objects.filter(author_name__icontains=input_value).exists():
                author = Author.objects.prefetch_related('posts').get(author_name__icontains=input_value)
                is_author = True
            if Post.objects.filter(title__icontains=input_value).exists():
                posts = Post.objects.filter(title__icontains=input_value)

    context = {
        'posts': posts,
        'author': author,
        'is_author': is_author,
        'is_title': is_title,
    }
    
    return render(request, 'blog/blogpage.html', context)


@login_required
def Blog_Chat(request):
    room_name = request.GET.get('room_name') or None # lấy tên phòng nếu có
    otherauthor_name = request.GET.get('author_name') or None # lấy tên người cần chat cùng
    current_user = request.user

    room = None
    chat_messages = []
    error_message = ""
    current_author = None
    otherauthor = None
    room_id = None

    
    if room_name:
        try:
            room = Room.objects.get(room_name=room_name)
        except Room.DoesNotExist:
            room = None
    elif otherauthor_name:
        try:
            otherauthor = Author.objects.get(author_name=otherauthor_name)
        except Author.DoesNotExist:
            messages.warning(request, "Người dùng không tồn tại!")
            error_message = "Người dùng không tồn tại!"

        try:
            current_author = current_user.author
        except Author.DoesNotExist:
            messages.warning(request, "Bạn chưa có quyền tác giả!")
            error_message = "Bạn chưa có quyền tác giả!"

        if current_author and otherauthor and current_author == otherauthor:
            messages.warning(request, "Không thể chat với chính mình!")
            error_message = "Không thể chat với chính mình!"

        if error_message:
            return render(request, 'blog/blogchat.html', {
                'error_message': error_message,
                'chat_messages': [],
                'current_username': current_user.username,
            })

        if otherauthor and current_author:
            members_set = {current_author.id, otherauthor.id}

            possible_rooms = (
                Room.objects
                .filter(room_type='private', room_members__id=current_author.id)
                .annotate(member_count=Count('room_members'))
                .filter(member_count=2)
                .distinct()
            )

            room = next(
                (r for r in possible_rooms if set(r.room_members.values_list('id', flat=True)) == members_set),
                None
            )
            if not room:
                room = Room.objects.create(room_name=None, room_type='private')
                room.room_members.add(current_author, otherauthor)

    if room:
        chat_messages = Message.objects.filter(room=room).select_related('author').order_by('date')
        room_id = room.pk

    context = {
        'current_author_name': current_author.author_name if current_author else None,
        'chat_messages': chat_messages,
        'room_id': room_id,
    }
    return render(request, "blog/blogchat.html", context)





 



class Blog_List(ListView):
    model = Post
    template_name = 'blog/bloglist.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = self.request.GET.get('data')
        if data:
            queryset = queryset.filter(
                Q(author__author_name__icontains=data)|
                Q(title__icontains=data))
        return queryset


class Post_Create(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/postcreate.html'
    form_class = PostForm
    success_url = reverse_lazy("bloglist")

    def form_valid(self, form):
        user = self.request.user
        # tạo Author nếu chưa có
        if not hasattr(user, 'author'):
            Author.objects.create(user=user, author_name=user.username)
        form.instance.author = user.author
        return super().form_valid(form)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']



        
    









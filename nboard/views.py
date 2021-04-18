from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm


# 사용하지 않는 코드
# profile에서 postlist가 쓰임
class PostListView(ListView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            qs = Post.objects.all() \
                .filter(
                Q(author__in=request.user.following_set.all()) |
                Q(author=request.user)
            )
            if qs:
                paginator, page, queryset, is_paginated = super().paginate_queryset(qs, 9)
                context = {
                    'paginator': paginator,
                    'page': page,
                    'is_paginated': is_paginated,
                    'post_list': queryset,
                }
                return render(request, 'nboard/post_list.html', context)
        return render(request, 'nboard/post_list.html', {
            'post_list': None
        })


# post 생성뷰
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    # post로 받은 form이 유효하다면
    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.author = self.request.user # form에 넣지 않은 author를 request.user로 지정
        new_form.save()
        new_form.tag.add(*new_form.extract_tag_list()) # 해쉬태그 형식으로 적은 내용들 tag에 add
        messages.success(self.request, '포스팅 저장 완료')
        return super().form_valid(form)


# post update view
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    # update 요청시
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, pk=kwargs['pk'])
        # 작성한 회원이 아니라면
        if self.object.author != request.user:
            messages.warning(self.request, '작성한 회원만 수정할 수 있습니다')
            # 기존 detailview로 이동
            return redirect(self.object)
        form = PostForm
        return super(PostUpdateView, self).get(form)

    # update한 form이 유효하다면
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # 요청한 회원이 post의 작성자와 같다면
        if self.object.author == self.request.user:
            messages.success(self.request, '포스팅 수정 완료')
            form.save()
            # 해쉬태그로 적힌 tag들 set하여 재 지정
            self.object.tag.set(self.object.extract_tag_list())
        # 아니라면 return
        else:
            messages.warning(self.request, '작성한 회원만 수정할 수 있습니다')
        return super().form_valid(form)


# post delect view
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name_suffix = '_delete'        # _delete가 들어간 html file을 template으로 지정
    success_url = 'nboard/post_list.html'
    
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, pk=kwargs['pk'])
        # 작성한 회원이 아니라면 return detail view
        if self.object.author != request.user:
            messages.warning(self.request, '작성한 회원만 삭제할수 있습니다')
            return redirect(self.object)
        return super(PostDeleteView, self).get(Post)

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, pk=kwargs['pk'])
        # 작성한 회원이 아니라면 return detail view
        if self.object.author != request.user:
            messages.warning(self.request, '작성한 회원만 삭제할수 있습니다')
            return redirect(self.object)
        # 맞다면 post delete
        self.object.delete()
        messages.success(request, '포스팅 삭제 완료')
        # profile로 이동
        return redirect('accounts:profile')


# post detail view
class PostDetailView(DetailView):
    model = Post

    # post와 comment를 같이 넣기 위해서 comment conetext 추가
    def get_context_data(self, **kwargs):
        comment_list = Comment.objects.filter(post=kwargs.get('object'))
        comment_form = CommentForm()
        context = {
            'comment_list': comment_list,
            'form': comment_form
        }
        return super().get_context_data(**context)

    # comment 저장 post
    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = super().get_object()
            comment.save()
            return redirect('nboard:post_detail', pk=kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', '')  # comment 수정에 쓰일 comment.pk
        # comment pk값이 넘어왔다면
        if pk:
            comment = Comment.objects.get(pk=pk)
            if comment.author != request.user:
                messages.warning(request, message="작성자가 아닙니다")
                return
            # 기존 object를 가져와서 저장
            self.object = self.get_object()
            # comment update에 쓰일 comment initial dict 미리 생성
            # 사실 author와 post는 필요없음
            # 왜냐하면 form엔 comment만 쓰이기 때문에...
            initial_dict = {
                "comment": comment.comment,
                "author": comment.author,
                "post": comment.post,
            }
            # 수정을 위해 comment form에 initial로 comment를 넣어줌
            form = CommentForm(request.POST or None, initial=initial_dict)
            self.object = self.get_object()
            # context에 comment를 넗은 comment_form을 넣고 return
            context = self.get_context_data(object=self.object)
            context["comment_edit_form"] = form
            context["comment_pk"] = comment.pk

            return self.render_to_response(context)
        else:
            # 수정이 아니라면 기본 object를 return
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)

        return self.render_to_response(context)


# 글 좋아요 기능
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 본인 글은 제외
    if request.user==post.author:
        messages.warning(request, "작성한 회원은 좋아요를 누를수 없습니다")
        return redirect('nboard:post_detail', pk=pk)
    post.like_user.add(request.user)
    messages.success(request, f"{post.author} 좋아요")
    # 요청한 링크로 redirect
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


# 글 좋아요 취소 기능
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user.remove(request.user)
    messages.success(request, f"{post.author} 좋아요 취소")
    # 요청한 링크로 redirect
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


# 댓글 삭제기능
# post_detail로 돌아가기 위한 post.pk와
# 삭제하기위한 comment.pk를 같이 받는다
def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('nboard:post_detail', pk=pk)


# 댓글 수정기능
# post_detail로 돌아가기 위한 post.pk와
# 수정하기위한 comment.pk를 같이 받는다
def comment_edit(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    form = CommentForm(request.POST or None,
                       instance=comment)
    if request.method == 'POST':
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.comment = request.POST.get("comment")
            comment_form.save()

    return redirect('nboard:post_detail', pk=pk)


# CBV기반 as_view()
post_create = PostCreateView.as_view()
post_update = PostUpdateView.as_view()
post_list = PostListView.as_view()
post_delete = PostDeleteView.as_view()


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from .models import Profile, User
from nboard.models import Post


# 로그인 뷰
# redirect는 기본적으로 profile로 지정되어 있으므로 미지정
class LoginView(LoginView):
    model = get_user_model()
    template_name = 'accounts/login.html'


# 로그아웃 뷰
# 로그아웃시 login 페이지로 이동
class LogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


login_view = LoginView.as_view()
logout_view = LogoutView.as_view()


# 회원가입 함수
def signup_view(request):
    # POST 일땐 login 시도
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserForm
    # GET 일땐 회원가입 form 리턴
    return render(request, 'accounts/signup.html', {
        'form': form,
    })


# profile view
@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user_id=request.user.pk)
    # 팔로우 한 유저와 내가 쓴 post만 담음
    post_list = Post.objects.all() \
        .filter(
        Q(author__in=request.user.following_set.all()) |
        Q(author=request.user)
    )
    # 로그인 한 유저의 profile과 post_list 리턴
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'post_list': post_list,
    })


# profile update
@login_required
def profile_edit(request):
    if request.POST:
        # 함수방식에선 파일도 보낼 시 request.POST, request.FILES가 포함되어야함
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
        return redirect('accounts:profile')

    # update를 하기 위해 본인의 profile을 form의 instance로 담아 리턴해줌
    profile = Profile.objects.get(pk=request.user.pk)
    profile_form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit_form.html', {
        'form': profile_form,
    })


# follow 추천
@login_required
def follow_recommend(request):
    profile = get_object_or_404(Profile, user_id=request.user.pk)
    # 나와 팔로우 한 user를 제외한 나머지를 suggested_user_list로 담음
    suggested_user_list = get_user_model().objects.all() \
        .exclude(pk=request.user.pk) \
        .exclude(pk__in=request.user.following_set.all())

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'suggested_user_list': suggested_user_list
    })


# 팔로우 되어있는 user 리스트
@login_required
def follower_list(request):
    profile = get_object_or_404(Profile, user_id=request.user.pk)
    # 나와 내가 팔로한 유저만 filter 하려 follower_list에 저장
    follower_list = get_user_model().objects.all() \
        .exclude(pk=request.user.pk) \
        .filter(pk__in=request.user.following_set.all())

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'follower_list': follower_list
    })


# user follow 기능
@login_required
def user_follow(request, username):
    follow_user = get_object_or_404(User, username=username, is_active=True)
    request.user.following_set.add(follow_user)
    follow_user.follower_set.add(request.user)
    messages.success(request, f"{follow_user}님을 팔로우 했습니다.")
    # 요청한 주소로 다시 redirect
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


# user unfollow 기능
@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username, is_active=True)
    request.user.following_set.remove(unfollow_user)
    unfollow_user.follower_set.remove(request.user)
    messages.success(request, f"{unfollow_user}님을 언팔로우 했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

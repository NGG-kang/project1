from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('follow_recommend/', views.follow_recommend, name='follow_recommend'),
    path('follower_list/', views.follower_list, name='follower_list'),
    re_path(r'^(?P<username>[\w.@+-]+)/follows/$', views.user_follow, name='user_follow'),
    re_path(r'^(?P<username>[\w.@+-]+)/unfollows/$', views.user_unfollow, name='user_unfollow'),

]
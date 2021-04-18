from django.urls import path, include, re_path
from . import views

app_name = 'nboard'



urlpatterns = [
    path('post_create/', views.post_create, name='post_create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
    path('<int:pk>/comment_edit/<int:comment_pk>/', views.comment_edit, name='comment_edit'),
    path('<int:pk>/post_update/', views.post_update, name='post_update'),
    path('<int:pk>/post_delete/', views.post_delete, name='post_delete'),
    path('<int:pk>/post_like/', views.post_like, name='post_like'),
    path('<int:pk>/post_unlike/', views.post_unlike, name='post_unlike'),
]

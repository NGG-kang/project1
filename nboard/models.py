from django.db import models
from django.conf import settings
from django.urls import reverse
import re


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(max_length=300)
    photo = models.ImageField(upload_to="nboard/post/%Y/%m/%d", blank=True)
    tag = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_post_set", blank=True)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('nboard:post_detail', args=[self.pk])

    def is_like_user(self, user):
        return self.like_user.filter(pk=user.pk).exists()

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.message)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name



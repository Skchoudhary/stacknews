from django.contrib.auth.models import User
from django.forms import ModelForm

from dashboard.models import Post, Comment


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name')


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'url', 'post_text', 'post_type', 'created_by')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('post', 'comment_text', 'user')

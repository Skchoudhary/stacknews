from django.contrib.auth.models import User
from django.forms import ModelForm

from dashboard.models import Post


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'name')


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'url', 'post_text', 'post_type', 'created_by')

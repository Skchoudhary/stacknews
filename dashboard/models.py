from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, URLField, IntegerField, BooleanField
from django.utils import timezone
from django.urls import reverse

# CONSTANTS
POST_TYPE = (("P", "Post"), ("J", "Job Post"), ("AMA", "Ask Me Anything"))


class BasicDetails(models.Model):
    """
    Common fields to all models
    """

    creation_date = models.DateTimeField(default=timezone.now)
    last_modification_date = models.DateTimeField(auto_now=True)

    is_active = BooleanField(default=True)
    to_show = BooleanField(default=True)

    class Meta:
        abstract = True


class Post(BasicDetails):
    """
    Models to save basic info regarding the post
    """

    created_by = models.ForeignKey(User, null=False)

    title = CharField(max_length=1000, default="", blank=True)
    url = URLField(max_length=1000, default="", blank=True)
    post_text = CharField(max_length=5000, default="", blank=True)
    post_type = CharField(max_length=30, default="P", choices=POST_TYPE)


class Comment(BasicDetails):
    """
    Details about the comment on the post.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")

    comment_text = CharField(max_length=3000, default="", blank=True)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return reverse("comment_detail", args=[str(self.id)])


class KarmaPoint(BasicDetails):
    """
    Count of the star/applause of the post.
    """

    post = models.ForeignKey(Post, related_name="%(class)s_karma_post", null=False)
    user = models.ForeignKey(User, null=False)

    count = IntegerField(default=0, null=False)

    def __str__(self):
        return self

    def get_absolute_url(self):
        return reverse("karma_point", args=[str(self.id)])

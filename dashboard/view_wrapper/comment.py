import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect
from dashboard.forms import CommentForm

# Constants
logger = logging.getLogger(__name__)
base_filter = Q(is_active=True) & Q(to_show=True)


@login_required(login_url="/dashboard/login/")
def comment(request):
    """
    Comment save method against a post.
    :param request:
    :return:
    """
    comment_text = request.POST.get("comment", "")
    linked_post = request.POST.get("linked_post", "")

    comment_is_valid = CommentForm(
        {"post": linked_post, "comment_text": comment_text, "user": request.user.id}
    )

    if comment_is_valid.is_valid():
        comment_is_valid.save()
    else:
        logger.info("Comment data is invalid " + str(comment_is_valid.errors))

    return redirect("/")

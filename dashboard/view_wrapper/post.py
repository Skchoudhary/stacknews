import logging

from django.contrib.auth.decorators import (login_required)
from django.db.models import (Q)
from django.shortcuts import redirect
from dashboard.forms import (PostForm)
from dashboard.models import Post

# Constants
logger = logging.getLogger(__name__)
base_filter = (Q(is_active=True) & Q(to_show=True))


@login_required(login_url='/dashboard/login/')
def add_post(request):
    """

    :param request:
    :return:
    """
    response = {'status': 'failure'}

    post_data = PostForm({'post_type': request.POST.get('post_type', 'P'), 'title': request.POST.get('post_title', ''), 'post_text': request.POST.get('post_text', ''), 'url': request.POST.get('post_URL', ''), 'created_by': request.user.id})
    if post_data.is_valid():
        post_data.save()
        response['status'] = 'success'
    else:
        logger.error('Error while saving the post ' + str(post_data.errors))

    return redirect('/')


@login_required(login_url='/dashboard/login/')
def remove_post(request):
    """

    :param request:
    :return:
    """
    post_id = request.POST.get('post_id', '')
    post_obj = Post.objects.filter(base_filter).filter(post_type='P').filter(pk=post_id)

    if post_obj:
        post_obj.update(active=0, to_show=0)

    return redirect('/dashboard/landing_view')


import json

from django.http import HttpResponse
from django.shortcuts import render
from dashboard.models import Post


def latest_post(request):
    """
    Fetch latest post shared
    :param request:
    :return:
    """
    post_obj = Post.objects.filter(is_active=True).filter(to_show=True).order_by('-creation_date')

    post_list = [{'text': post.post_text, 'url': post.url, 'created_by': post.created_by} for post in post_obj]

    return HttpResponse(json.dumps({'flag': 'error'}), content_type='application/json')

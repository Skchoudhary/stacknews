import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import redirect, render
from dashboard.forms import UserForm, PostForm
from dashboard.models import Post


def latest_post(request):
    """
    Fetch latest 20 post shared
    :param request:
    :return:
    """
    post_obj = Post.objects.filter(is_active=True).filter(to_show=True).order_by('-creation_date')[:20]

    return render(request, 'dashboard/main_post.html', {'post_obj': post_obj})


def add_post(request):
    """

    :param request:
    :return:
    """
    response = {'status': 'failure'}

    post_data = PostForm({'post_url': request.POST.get('post_type', 'P'), 'title': request.POST.get('post_title', ''), 'post_text': request.POST.get('post_text', ''), 'url': request.POST.get('post_URL', ''), 'created_by_id': request.user})
    if post_data.is_vald():
        post_data.save()
        response['status'] = 'success'

    return redirect('/dashboard/landing_view')


def remove_post(request):
    """

    :param request:
    :return:
    """
    post_id = request.POST.get('post_id', '')
    post_obj = Post.objects.filter(Q(to_show=1) & Q(active=1)).filter(pk=post_id)

    if post_obj:
        post_obj.update(active=0, to_show=0)

    return redirect('/dashboard/landing_view')


def create_new_user(request):
    """

    :param request:
    :return:
    """

    user_id = request.POST.get('user_id', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    name = request.POST.get('name', '')
    msg = {}

    if user_id and password and email:
        user_detail = UserForm({'email': email, 'password': password, 'username': user_id, 'name': name})

        if user_detail.is_valid():
            user_detail.save()
            msg['user_id'] = user_detail
            msg['status'] = 'success'
        else:
            msg['status'] = 'failure'

        return HttpResponse(json.dumps(msg), content_type='application/json')


def update_password(request):
    """

    :param request:
    :return:
    """

    user_id = request.POST.get('user_id', '')
    old_password = request.POST.get('old_password', '')
    new_password = request.POST.get('new_password', '')
    response = {
        'status': 'failure',
        'wrong_password': 1,
        'empty_password': 1
    }
    if User.objects.filter(Q(to_show=1) & Q(active=1)).filter(username=user_id):
        user = authenticate(username=user_id, password=old_password)
        if user:
            response['wrong_password'] = 0
            if new_password:
                user.set_password(new_password)
                user.save()
                response['empty_password'] = 1
                response['status'] = 'success'
            auth_login(request, user)

        return HttpResponse(json.dumps(response), content_type='application/json')


def remove_user(request):

    user_id = request.POST('user_id', '')
    user_details = User.objects.filter(Q(to_show=1) & Q(active=1)).filter(username=user_id)
    response = {'status': 'failure'}

    if user_details:
        user_details.update(active=0, to_show=0)
        response['status'] = 'success'

    return HttpResponse(json.dumps(response), content_type='application/json')


def login(request):
    """

    :param request:
    :return:
    """
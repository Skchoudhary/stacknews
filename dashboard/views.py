import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout, login
from django.shortcuts import redirect, render
from dashboard.forms import UserForm, PostForm
from dashboard.models import Post


# Constants
logger = logging.getLogger(__name__)


def latest_post(request):
    """
    Fetch latest 20 post shared
    :param request:
    :return:
    """
    logger.info('In method Latest Post')
    post_obj = Post.objects.filter(is_active=True).filter(to_show=True).order_by('-creation_date')[:20]
    logger.info('Post Obj' + str(post_obj))
    return render(request, 'dashboard/main_post.html', {'post_obj': post_obj})


@login_required(login_url='/')
def add_post(request):
    """

    :param request:
    :return:
    """
    response = {'status': 'failure'}

    logger.info('Title ::' + str(request.POST['post_title']))

    logger.info('data request ::' + str({'post_type': request.POST.get('post_type', 'P'), 'title': request.POST.get('post_title', ''), 'post_text': request.POST.get('post_text', ''), 'url': request.POST.get('post_URL', ''), 'created_by': request.user.id}))

    post_data = PostForm({'post_type': request.POST.get('post_type', 'P'), 'title': request.POST.get('post_title', ''), 'post_text': request.POST.get('post_text', ''), 'url': request.POST.get('post_URL', ''), 'created_by': request.user.id})
    if post_data.is_valid():
        post_data.save()
        response['status'] = 'success'
    else:
        logger.error('Error while saving the post ' + str(post_data.errors))

    return redirect('/')


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

    user_id = request.POST.get('user_name', '')
    password = request.POST.get('password', '')
    name = request.POST.get('user_name', '')
    msg = {}

    if user_id and password:
        user_detail = UserForm({'password': password, 'username': user_id, 'first_name': name})

        if user_detail.is_valid():
            user_detail = User.objects.create_user(**user_detail.cleaned_data)
            # user_detail.save()
            msg['user_id'] = user_detail
            msg['status'] = 'success'
        else:
            msg['status'] = 'failure'
            logger.info('Error while creating user :' + str(user_detail.errors))

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


def login_view(request):
    """

    :param request:
    :return:
    """
    logger.info('new login page request12')
    return render(request, 'dashboard/login.html')


def stocknews_login(request):
    """
    Method to authenticate the user.
    :param request:
    :return:
    """
    request_type = request.POST.get('form_type', '')

    if request_type == 'new_user':
        create_new_user(request)

    elif request_type == 'login':

        username = request.POST.get('user_name', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')

        else:
            logger.error("Authentication failed" + str(password) + str(username))
            return render(request, 'dashboard/login.html', {'error_msg': 'Authentication failed', })


# @login_required(login_url='/login/')
def new_post(request):
    """
    
    :param request: 
    :return: 
    """

    return render(request, 'dashboard/submit.html')

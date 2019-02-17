import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout

from dashboard.forms import UserForm
from dashboard.models import Post


def latest_post(request):
    """
    Fetch latest post shared
    :param request:
    :return:
    """
    post_obj = Post.objects.filter(is_active=True).filter(to_show=True).order_by('-creation_date')[:20]

    post_list = [{'text': post.post_text, 'url': post.url, 'created_by': post.created_by} for post in post_obj]

    return HttpResponse(json.dumps({'flag': 'error'}), content_type='application/json')


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

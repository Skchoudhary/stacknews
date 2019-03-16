from django.conf.urls import url, include
from dashboard.views import latest_post, create_new_user, login

ajax_url = [
    url(r'^fetch_latest_post/', latest_post, name='latest_post')
]

urlpatterns = [

    url(r'^$', latest_post, name='dashboard_page'),
    url(r'^post_submit', latest_post, name='post_submit'),
    url(r'^create_new_user', create_new_user, name='create_new_user'),
    url(r'^login', login, name='login'),
    url(r'^api/', include(ajax_url)),
]

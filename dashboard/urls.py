from django.conf.urls import url, include
from dashboard.views import latest_post, create_new_user, stocknews_login, new_post, add_post, login_view

ajax_url = [
    url(r'^fetch_latest_post/', latest_post, name='latest_post')
]

urlpatterns = [

    url(r'^$', latest_post, name='dashboard_page'),
    url(r'^post_submit/$', add_post, name='post_submit'),
    url(r'^create_new_user/$', create_new_user, name='create_new_user'),
    url(r'^view_login/$', login_view, name='view_login'),
    url(r'^login/$', stocknews_login, name='login'),
    url(r'^api/$', include(ajax_url)),
    url(r'^new_post_page/$', new_post, name='new_post'),
]

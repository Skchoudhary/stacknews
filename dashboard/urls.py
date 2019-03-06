from django.conf.urls import url, include
from dashboard.views import latest_post

ajax_url = [
    url(r'^fetch_latest_post/', latest_post, name='latest_post')
]

urlpatterns = [

    url(r'^$', latest_post, name='dashboard_page'),
    url(r'^api/', include(ajax_url)),
]

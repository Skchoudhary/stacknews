from django.conf.urls import url, include

ajax_url = [
    url(r'^fetch_latest_post/', latest_post, name='latest_post')
]

urlpatterns = [

    url(r'^api/', include(ajax_url)),
]

from django.conf.urls import url, include

from dashboard.view_wrapper.comment import comment
from dashboard.view_wrapper.post import add_post
from dashboard.views import (
    latest_post,
    create_new_user,
    stacknews_login,
    new_post,
    log_out,
    render_comment_page,
    view_login,
)


ajax_url = [url(r"^fetch_latest_post/", latest_post, name="latest_post")]

urlpatterns = [
    url(r"^$", latest_post, name="dashboard_page"),
    url(r"^post_submit/$", add_post, name="post_submit"),
    url(r"^comment/$", comment, name="comment"),
    url(r"^render_comment_page/$", render_comment_page, name="render_comment_page"),
    url(r"^create_new_user/$", create_new_user, name="create_new_user"),
    url(r"^login/$", stacknews_login, name="login"),
    url(r"^logout/$", log_out, name="logout"),
    url(r"view_login/$", view_login, name="login_page"),
    url(r"^api/$", include(ajax_url)),
    url(r"^new_post_page/$", new_post, name="new_post"),
]

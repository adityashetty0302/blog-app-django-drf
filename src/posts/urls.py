from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    # url(r'^posts/$', "<appname>.views.<function_name>"),

    url(r'^posts/api/$', PostListAPIView.as_view(), name='listapi'),
    url(r'^posts/api/create/$', PostCreateAPIView.as_view(), name='createapi'),
    url(r'^posts/api/(?P<id>[\w-]+)/$', PostDetailAPIView.as_view(),
        name='detailapi'),
    url(r'^posts/api/(?P<id>[\w-]+)/edit/$', PostUpdateAPIView.as_view(),
        name='updateapi'),
    url(r'^posts/api/(?P<id>[\w-]+)/delete/$', PostDeleteAPIView.as_view(),
        name='deleteapi'),
]

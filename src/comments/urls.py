from django.conf.urls import url
from django.contrib import admin

from .views import (comment_thread, comment_delete, CommentListAPIView,
                    CommentDetailAPIView)

urlpatterns = [
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),

    url(r'^api/$', CommentListAPIView.as_view(), name='comments_list_api'),
    url(r'^api/(?P<id>\d+)/$', CommentDetailAPIView.as_view(),
        name='comments_detail_api'),
]

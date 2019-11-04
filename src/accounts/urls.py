from django.conf.urls import url
from .views import (UserCreateAPIView, UserLoginAPIView)

urlpatterns = [
    url(r'^api/register$', UserCreateAPIView.as_view(), name='register'),
    url(r'^api/login', UserLoginAPIView.as_view(), name='login'),
]

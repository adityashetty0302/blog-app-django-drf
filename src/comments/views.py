try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Comment

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone

from rest_framework import generics
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from posts.pagination import PostLimitOffsetPagination, \
    PostPageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser,
                                        IsAuthenticatedOrReadOnly)
from .serializers import (CommentListSerializer, CommentDetailSerializer)


@login_required  # (login_url='/login/') #LOGIN_URL = '/login/'
def comment_delete(request, id):
    # obj = get_object_or_404(Comment, id=id)
    # obj = CommentFormmment.objects.get(id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if obj.user != request.user:
        # messages.success(request, "You do not have permission to view this.")
        # raise Http404
        reponse = HttpResponse("You do not have permission to do this.")
        reponse.status_code = 403
        return reponse
        # return render(request, "confirm_delete.html", context, status_code=403)

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "object": obj
    }
    return render(request, "confirm_delete.html", context)


def comment_thread(request, id):
    # obj = Comment.objects.get(id=id)
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    if not obj.is_parent:
        obj = obj.parent

    content_object = obj.content_object  # Post that the comment is on
    content_id = obj.content_object.id

    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(
            new_comment.content_object.get_absolute_url())

    context = {
        "comment": obj,
        "form": form,
    }
    return render(request, "comment_thread.html", context)


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()
    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ['title', 'content', 'user__first_name']
    # pagination_class = PostPageNumberPagination  # PageNumberPagination
    #
    # def get_queryset(self, *args, **kwargs):
    #     queryset_list = Post.objects.all()
    #     query = self.request.GET.get("q")
    #     if query:
    #         queryset_list = queryset_list.filter(
    #             Q(title__icontains=query) |
    #             Q(content__icontains=query) |
    #             Q(user__first_name__icontains=query) |
    #             Q(user__last_name__icontains=query)
    #         ).distinct()
    #     return queryset_list


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin,
                           generics.RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# class PostDeleteAPIView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'slug'

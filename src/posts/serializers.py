from rest_framework import serializers
from posts.models import Post
from comments.models import Comment
from comments.serializers import CommentListSerializer
from accounts.serializers import UserDetailSerializer


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'publish']


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'slug', 'content', 'publish']

    def get_user(self, obj):
        return str(obj.user.username)


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['user', 'id', 'title', 'slug', 'content', 'publish',
                  'comments']

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentListSerializer(c_qs, many=True).data
        return comments

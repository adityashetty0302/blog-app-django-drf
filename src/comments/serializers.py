from rest_framework import serializers
from comments.models import Comment
from accounts.serializers import UserDetailSerializer


class CommentListSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'reply_count']

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_user(self, obj):
        return str(obj.user.username)


class CommentChildSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'timestamp']


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'timestamp', 'reply_count',
                  'replies', ]
        read_only_fields = ['reply_count', 'replies', ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

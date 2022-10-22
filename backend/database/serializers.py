from rest_framework import serializers  
from .models import Authors, Posts, Followers, FollowRequests, Comments, Likes, LikesComments, Liked, Inbox
class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = [
            'id',
            'type',
            'host',
            'displayName',
            'url',
            'github',
            'accepted',
            'profileImage'
        ]

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = [
            'id',
            'type',
            'title',
            'source',
            'origin',
            'description',
            'contentType',
            'content',
            'author',
            'count',
            'published',
            'visibility',
            'unlisted'
        ]

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = [
            'id',
            'followed',
            'follower',
        ]

class FollowRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequests
        fields = [
            'id',
            'receiver',
            'requester'
        ]

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        models = Comments
        fields = [
            'id',
            'type',
            'author',
            'comment',
            'contentType',
            'published',
        ]

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = [
            'id',
            'context',
            'summary',
            'type',
            'published'
            'author',
            'post'
        ]

class LikesCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = [
            'id',
            'context',
            'summary',
            'type',
            'published'
            'author',
            'comment'
        ]

class LikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields = [
            'id',
            'author',
            'like'
        ]

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = [
            'id',
            'author',
            'post'
        ]


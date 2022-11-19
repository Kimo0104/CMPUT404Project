from rest_framework import serializers  

from django.contrib.auth.models import User
from .models import Authors, Images, Posts, Followers, FollowRequests, Comments, Likes, LikesComments, Inbox
from .models import Authors, Posts, Followers, FollowRequests, Comments, Likes, LikesComments, Inbox


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

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
            'profileImage',
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
            'originalAuthor',
            'author',
            'count',
            'published',
            'visibility'
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
        model = Comments
        fields = [
            'id',
            'type',
            'author',
            'post',
            'comment',
            'contentType',
            'published'
        ]

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = [
            'id',
            'context',
            'summary',
            'type',
            'published',
            'author',
            'post'
        ]

class LikesCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesComments
        fields = [
            'id',
            'context',
            'summary',
            'type',
            'published',
            'author',
            'comment'
        ]

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = [
            'id',
            'author',
            'post'
        ]

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'id',
            'imageContent',
            'referenceId'
        ]

from rest_framework import serializers  
from .models import Authors, Posts, Likes, Comments, Follows

class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = [
            'id',
            'host',
            'display_name',
            'github_url',
            'profile_image',
            'username',
            'password',
            'accepted'
        ]

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = [
            'id',
            'title',
            'description_type',
            'description',
            'date',
            'image_url',
            'author'
        ]

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = [
            'id',
            'liker',
            'post'
        ]

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        models = Comments
        fields = [
            'id',
            'comment',
            'commenter',
            'post'
        ]

class FollowsSerializer(serializers.ModelSerializer):
    class Meta:
        models = Follows
        fields = [
            'id',
            'relationship_state'
            'author',
            'foreign_author'
        ]
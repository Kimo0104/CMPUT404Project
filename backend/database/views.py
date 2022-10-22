from urllib.robotparser import RequestRate
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

#Models defines how their objects are stored in the database
#serializers defines how to convert a post object to JSON
from .models import Posts, Comments, Likes, Liked, Inbox
from .serializers import PostsSerializer, CommentsSerializer, LikesSerializer, LikedSerializer, InboxSerializer

class PostsAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID/posts/{POST_ID}
    #get the public post whose id is POST_ID
    @action(detail=True, methods=['get'],)
    def getPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        print(authorId, postId)
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    #POST service/authors/{AUTHOR_ID/posts/{POST_ID}
    #update the post whose id is POST_ID (must be authenticated)
    @action(detail=True, methods=['post'],)
    def updatePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    #DELETE service/authors/{AUTHOR_ID/posts/{POST_ID}
    #remove the post whose id is POST_ID
    @action(detail=True, methods=['delete'],)
    def deletePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    #PUT service/authors/{AUTHOR_ID/posts/{POST_ID}
    #create a post where its id is POST_ID
    @action(detail=True, methods=['put'],)
    def createPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    #GET service/authors/{AUTHOR_ID}/posts/{POST_ID}/image
    #get the public post converted to binary as an image
    @action(detail=True, methods=['get'],)
    def getImagePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

class CommentsAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    #get the list of comments of the post whose id is POST_ID
    @action(detail=True, methods=['get'],)
    def getComments(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Comments.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)

    #POST service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    #if you post an object of “type”:”comment”, it will add your comment to the post whose id is POST_ID
    @action(detail=True, methods=['post'],)
    def createComment(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Comments.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)

class LikesAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    #a list of likes from other authors on AUTHOR_ID’s post POST_ID
    @action(detail=True, methods=['get'],)
    def getPostLikes(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Likes.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = LikesSerializer(queryset, many=True)
        return Response(serializer.data)

    #GET service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    #a list of likes from other authors on AUTHOR_ID’s post POST_ID comment COMMENT_ID
    @action(detail=True, methods=['get'],)
    def getCommentLikes(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        commentId = kwargs["commentId"]
        print(authorId, postId, commentId)
        queryset = Likes.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = LikesSerializer(queryset, many=True)
        return Response(serializer.data)

class LikedAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/liked
    #list what public things AUTHOR_ID liked
    @action(detail=True, methods=['get'],)
    def getAuthorLiked(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        queryset = Liked.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = LikedSerializer(queryset, many=True)
        return Response(serializer.data)

class InboxAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/inbox
    #if authenticated get a list of posts sent to AUTHOR_ID (paginated)
    @action(detail=True, methods=['get'],)
    def getInbox(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        queryset = Inbox.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = InboxSerializer(queryset, many=True)
        return Response(serializer.data)

    #POST service/authors/{AUTHOR_ID}/inbox
    #send a post to the author
    @action(detail=True, methods=['post'],)
    def sendPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        queryset = Inbox.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = InboxSerializer(queryset, many=True)
        return Response(serializer.data)

    #DELETE service/authors/{AUTHOR_ID}/inbox
    #clear the inbox
    @action(detail=True, methods=['delete'],)
    def deleteInbox(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        queryset = Inbox.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = InboxSerializer(queryset, many=True)
        return Response(serializer.data)



    

    






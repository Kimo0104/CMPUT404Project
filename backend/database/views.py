from urllib.robotparser import RequestRate
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
import json

#Models defines how their objects are stored in the database
#serializers defines how to convert a post object to JSON
from .models import Posts, Comments, Likes, Liked, Inbox
from .serializers import PostsSerializer, CommentsSerializer, LikesSerializer, LikedSerializer, InboxSerializer
import datetime

class PostsAPIs(viewsets.ViewSet):

    """-----------------------------------------------
    --------------------------------------------------
    ---------- START OF DEFAULT FUNCTIONS ------------
    --------------------------------------------------
    -----------------------------------------------"""  
    
    #GET posts/ will call this function
    def list(self, request):
        # define queryset to be the output of your query
        # pass the output to the serializer. If there's multiple rows in your output set many=True; otherwise False
        # return the data from the serializer
        queryset = Posts.objects.all()  
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

    #POST posts/ will call this function
    def create(self, request):
        #get info from request body
        body_unicode = request.body.decode('utf-8')
        body_dict = json.loads(body_unicode)

        #ensure required data exists
        if not ("title" in body_dict) or not ("author_id" in body_dict):
            return HttpResponseBadRequest

        #fill in non-required data with Nones
        if not "description_type" in body_dict:
            body_dict["description_type"] = None
        if not "description" in body_dict:
            body_dict["description"] = None
        if not "image_url" in body_dict:
            body_dict["image_url"] = None

        #set fields created in back-end
        body_dict["date"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        queryset = Posts.objects.create(
            title = body_dict["title"],
            description_type = body_dict["description_type"],
            description = body_dict["description"],
            date = body_dict["date"],
            image_url = body_dict["image_url"],
            author = body_dict["author"]
        )  
        serializer = PostsSerializer(queryset, many=False)
        return Response(serializer.data)

    #GET posts/{id} will call this function
    def retrieve(self, request, pk=None):
        queryset = Posts.objects.get(id = pk) 
        serializer = PostsSerializer(queryset, many=False)
        return Response(serializer.data)

    #PUT posts/{id} will call this function
    def update(self, request, pk=None):
        pass #I don't need this, so I won't implement


    #PATCH posts/{id} will call this function
    def partial_update(self, request, pk=None):
        #get existing post
        existingPost = Posts.objects.get(id = pk) 

        #get info from request body
        body_unicode = request.body.decode('utf-8')
        body_dict = json.loads(body_unicode)

        #update any fields passed to us
        if "title" in body_dict:
            existingPost.title = body_dict["title"]
        if "author_id" in body_dict:
            existingPost.author_id = body_dict["author_id"]
        if "description_type" in body_dict:
            existingPost.description_type = body_dict["description_type"]
        if "image_url" in body_dict:
            existingPost.image_url = body_dict["image_url"]
        if "date" in body_dict:
            existingPost.date = body_dict["date"]

        #save changes
        existingPost.save()
        
        serializer = PostsSerializer(existingPost, many=False)
        return Response(serializer.data)

    #DELETE posts/{id} will call this function
    def destroy(self, request, pk=None):
        return Posts.objects.get(id = pk).delete()
    
    """-----------------------------------------------
    --------------------------------------------------
    ---------- END OF DEFAULT FUNCTIONS --------------
    --------------------------------------------------
    -----------------------------------------------"""
    
    """-----------------------------------------------
    --------------------------------------------------
    --------- START OF SPECIFIC FUNCTIONS ------------
    --------------------------------------------------
    -----------------------------------------------"""

    #GET service/authors/{AUTHOR_ID/posts/{POST_ID}
    #get the public post whose id is POST_ID
    @action(detail=True, methods=['get'],)
    def getPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
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
    
    """-----------------------------------------------
    --------------------------------------------------
    --------- END OF SPECIFIC FUNCTIONS --------------
    --------------------------------------------------
    -----------------------------------------------"""

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

    #POST service/authors/{AUTHOR_ID}/inbox/
    #send a like object to AUTHOR_ID
    @action(detail=True, methods=['post'],)
    def sendLike(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        queryset = Likes.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = LikesSerializer(queryset, many=True)
        return Response(serializer.data)

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



    

    






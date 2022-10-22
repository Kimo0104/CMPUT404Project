from urllib.robotparser import RequestRate
import io
from rest_framework.parsers import JSONParser
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import io
from collections import defaultdict
from rest_framework.parsers import JSONParser
#Models defines how their objects are stored in the database
#serializers defines how to convert a post object to JSON
from .models import Authors, Posts, Comments, Likes, Liked, Inbox, Followers, FollowRequests
from .serializers import PostsSerializer, CommentsSerializer, LikesSerializer, LikesCommentsSerializer, InboxSerializer, FollowersSerializer, FollowRequestsSerializer

class PostsAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID/posts/{POST_ID}
    #get the public post whose id is POST_ID
    @action(detail=True, methods=['get'],)
    def getPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        try:
            post = Posts.objects.get(author = authorId, id = postId, visibility = Posts.PUBLIC)
        except Posts.DoesNotExist:
            post = None
        serializer = PostsSerializer(post)
        return Response(serializer.data)

    #POST service/authors/{AUTHOR_ID/posts/{POST_ID}
    #update the post whose id is POST_ID (must be authenticated)
    @action(detail=True, methods=['post'],)
    def updatePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        body = JSONParser().parse(io.BytesIO(request.body))
        post = Posts.objects.get(author = authorId, id = postId, visibility = Posts.PUBLIC)
        editableColumns = ["title", "description", "content"]
        edited = False
        for key, value in body.items():
            if key in editableColumns:
                setattr(post, key, value)
                edited = True
        if edited: post.save()
        return Response({"Success"}, status=status.HTTP_200_OK)

    #DELETE service/authors/{AUTHOR_ID/posts/{POST_ID}
    #remove the post whose id is POST_ID
    @action(detail=True, methods=['delete'],)
    def deletePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        Posts.objects.get(author = authorId, id = postId, visibility = Posts.PUBLIC).delete()
        return Response({"Success"}, status=status.HTTP_200_OK)

    #PUT service/authors/{AUTHOR_ID/posts/{POST_ID}
    #create a post where its id is POST_ID
    @action(detail=True, methods=['put'],)
    def createPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        body = defaultdict(lambda: None, JSONParser().parse(io.BytesIO(request.body)))
        post = Posts.objects.create(
            id = postId,
            type = body['type'],
            title = body['title'],
            source = body['source'],
            origin = body['origin'],
            description = body['description'],
            contentType = body['contentType'],
            content = body['content'],
            author = Authors.objects.get(id = authorId),
            published = body['published'],
            visibility = body['visibility'],
            unlisted = body['unlisted']
        )
        serializer = PostsSerializer(post)
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

#completed
class CommentsAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    #get the list of comments of the post whose id is POST_ID
    @action(detail=True, methods=['get'],)
    def getComments(self, request, *args, **kwargs):
        postId = kwargs["postId"]
        queryset = Comments.objects.filter(post_id=postId).order_by('-published')
        
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)

    #POST service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    #if you post an object of “type”:”comment”, it will add your comment to the post whose id is POST_ID
    @action(detail=True, methods=['post'],)
    def createComment(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]

        #check that contentType is a valid choice
        body = JSONParser().parse(io.BytesIO(request.body))
        contentType = None
        if 'contentType' in body:
            if body['contentBody'] == 'text/markdown':
                contentType = 'text/markdown'
            elif body['contentBody'] != 'text/plain':
                return Response({"Failed comment creation. Invalid input for contentBody."}, status=status.HTTP_400_BAD_REQUEST)

        if 'comment' in body:
            comment = str(body['comment'])
        else:
            return Response({"Failed comment creation. Missing 'comment' column."}, status=status.HTTP_400_BAD_REQUEST)

        Comments.objects.create(
            id = uuidGenerator(),
            author = authorId,
            post = postId,
            contentType = contentType,
            comment = comment
        )

        return Response({"Comment Created Successfully"}, status=status.HTTP_200_OK)

#completed
class LikesAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    #a list of likes from other authors on AUTHOR_ID’s post POST_ID
    @action(detail=True, methods=['get'],)
    def getPostLikes(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Likes.objects.filter(author_id=authorId, post_id=postId).order_by('-published')
        
        serializer = LikesSerializer(queryset, many=True)
        return Response(serializer.data)

    #GET service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    #a list of likes from other authors on AUTHOR_ID’s post POST_ID comment COMMENT_ID
    @action(detail=True, methods=['get'],)
    def getCommentLikes(self, request, *args, **kwargs):
        commentId = kwargs["commentId"]
        queryset = LikesComments.objects.filter(comment_id=commentId).order_by('-published')
        
        serializer = LikesCommentsSerializer(queryset, many=True)
        return Response(serializer.data)

#completed
class LikedAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/liked
    #list what public things AUTHOR_ID liked
    @action(detail=True, methods=['get'],)
    def getAuthorLiked(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]

        output = '{ "type":"liked", "items":['
        found = False
        for like in Liked.objects.filter(author_id=authorId).select_related('likes').order_by('-published'):
            output += LikesSerializer(like, many=False).data
            output += ','
            found = True
        
        if found:
            output = output[:len(output)-1]
        output +=']}'
        
        return Response(output, status=status.HTTP_200_OK)

#TODO getInbox, sendPost
class InboxAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/inbox
    #if authenticated get a list of posts sent to AUTHOR_ID (paginated)
    @action(detail=True, methods=['get'],)
    def getInbox(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        page = request.GET.get('page',1)
        size = request.GET.get('size',10)


        #get enough posts, sorted
        #get enough likes, sorted
        #get enough comments, sorted
        #iterate through each list, compiling them into a sorted inbox
        #paginate

        queryset = Inbox.objects.raw("""
            SELECT p.id, p.published AS date, "post" AS type
            FROM Inbox i
                LEFT OUTER JOIN Posts p
                    ON i.post_id = p.id
            WHERE i.author_id = {authorId}

            UNION

            SELECT l.id, l.published AS date, "like" AS type
            FROM Inbox i
                LEFT OUTER JOIN Likes l
                    ON i.post_id = l.post_id
            WHERE i.author_id = {authorId}

            UNION

            SELECT c.id, c.published AS date, "comment" AS type
            FROM Inbox i
                LEFT OUTER JOIN Comments c
                    ON i.post_id = c.post_id
            WHERE i.author_id = {authorId}
            ORDER BY date DESC
        """)
        
        serializer = InboxSerializer(queryset, many=True)
        return Response(serializer.data)

    #POST service/authors/{AUTHOR_ID}/inbox + /{POST_ID}
    #send a post to the author
    @action(detail=True, methods=['post'],)
    def sendPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]

        #check that authorId and postId exist
        if not Authors.objects.filter(id=authorId).count ==1 or not Posts.objects.filter(id=postId):
            return Response({"Tried to send an invalid post or send as an invalid author"}, status=status.HTTP_400_BAD_REQUEST)

        Inbox.objects.create(
            id = uuidGenerator(),
            author = authorId,
            post = postId
        )

        return Response({"Post Sent to Inbox Successfully"}, status=status.HTTP_200_OK)

    #DELETE service/authors/{AUTHOR_ID}/inbox
    #clear the inbox
    @action(detail=True, methods=['delete'],)
    def deleteInbox(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authorObj = Authors.objects.get(author_id=authorId)
        Inbox.objects.filter(author=authorObj).clear()
        
        return Response({"Delete Inbox Successful"}, status=status.HTTP_200_OK)

class FollowRequestsAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/followRequest
    #get all the people who want to follow AUTHOR_ID
    @action(detail=True, methods=['get'],)
    def getFollowRequests(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        queryset = FollowRequests.objects.raw("""
            YOUR SQL HERE
        """)
        serializer = FollowRequestsSerializer(queryset, many=True)
        return Response(serializer.data)

    #DELETE service/authors/{AUTHOR_ID}/followRequest/{FOREIGN_AUTHOR_ID}
    #remove FOREIGN_AUTHOR_ID's request to follow AUTHOR_ID (when AUTHOR_ID approve/deny a request)
    @action(detail=True, methods=['delete'],)
    def removeRequest(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        queryset = FollowRequests.objects.raw("""
            YOUR SQL HERE
        """)
        serializer = FollowRequestsSerializer(queryset, many=True)
        return Response(serializer.data)

    #POST service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #create FOREIGN_AUTHOR_ID's request to follow AUTHOR_ID
    @action(detail=True, methods=['post'],)
    def requestToFollow(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        queryset = FollowRequests.objects.raw("""
            YOUR SQL HERE
        """)
        serializer = FollowRequestsSerializer(queryset, many=True)
        return Response(serializer.data)
    
class FollowsAPIs(viewsets.ViewSet):

    #GET service/authors/{AUTHOR_ID}/followers
    #get all the followers of AUTHOR_ID
    @action(detail=True, methods=['get'],)
    def getFollowers(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        queryset = Followers.objects.raw("""
            YOUR SQL HERE
        """)
        serializer = FollowersSerializer(queryset, many=True)
        return Response(serializer.data)
    
    #GET /service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #check if FOREIGN_AUTHOR_ID is following AUTHOR_ID
    @action(detail=True, methods=['get'],)
    def checkFollower(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        queryset = Followers.objects.raw("""
            YOUR SQL HERE
        """)
        serializer = FollowersSerializer(queryset, many=True)
        return Response(serializer.data)

    #PUT service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    @action(detail=True, methods=['delete'],)
    def addFollower(self, request, *args, **kwargs):
        # Call {function} to delete the follower request record

        # Insert into Followers
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        queryset = Followers.objects.raw("""
            YOUR SQL HERE
        """)
        serializer = FollowersSerializer(queryset, many=True)
        return Response(serializer.data)

    #DELETE service/authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    @action(detail=True, methods=['delete'],)
    def removeFollower(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        queryset = Followers.objects.raw("""
            YOUR SQL HERE
        """)
        serializer = FollowersSerializer(queryset, many=True)
        return Response(serializer.data)



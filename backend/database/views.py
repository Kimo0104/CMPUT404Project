from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import io
from collections import defaultdict
from rest_framework.parsers import JSONParser
#Models defines how their objects are stored in the database
#serializers defines how to convert a post object to JSON
from .models import Posts, Comments, Likes, Liked, Inbox, Followers, FollowRequests, Authors
from .serializers import PostsSerializer, CommentsSerializer, LikesSerializer, LikedSerializer, InboxSerializer, FollowersSerializer, FollowRequestsSerializer

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
        return Response(serializer.data, status = status.HTTP_200_OK)

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



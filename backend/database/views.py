import io
import json
from datetime import datetime
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from collections import defaultdict
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Authors, Posts, Comments, Likes, LikesComments, Inbox, Followers, FollowRequests, Images, Users
from .serializers import AuthorsSerializer, ImageSerializer, PostsSerializer, CommentsSerializer, LikesSerializer, LikesCommentsSerializer, InboxSerializer, FollowersSerializer, FollowRequestsSerializer, UserSerializer
import uuid
import database
import ast
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import base64
import datetime

#pip install PyJWT
import jwt

import datetime
from datetime import datetime as dt

from django.views import View
import os
from django.conf import settings

remote_host = "https://cmput404-team13.herokuapp.com"

import uuid
def uuidGenerator():
    return str(uuid.uuid4())

def getCurrentDate():
    return dt.today().isoformat()

def expandPost(post):
    serializedPost = PostsSerializer(post).data
    # get the author of the post
    if not Authors.objects.filter(id=serializedPost["author"]).count() == 1:
        return Response("Tried to get comments from a post with a non-existent author", status=status.HTTP_400_BAD_REQUEST)
    # add the author object to the post object
    serializedPost["author"] = AuthorsSerializer(Authors.objects.get(id=serializedPost["author"])).data

    # get the original author of the post
    if not Authors.objects.filter(id=serializedPost["originalAuthor"]).count() == 1:
        return Response("Tried to get comments from a post with a non-existent original author", status=status.HTTP_400_BAD_REQUEST)
    # add the original author object to the post object
    serializedPost["originalAuthor"] = AuthorsSerializer(Authors.objects.get(id=serializedPost["originalAuthor"])).data

    return serializedPost

def expandComment(comment, serializedPost):
    serializedComment = CommentsSerializer(comment).data
    # add the post object to the comment objects
    serializedComment["post"] = serializedPost
    # get the author of the comment
    if not Authors.objects.filter(id=serializedComment["author"]).count() == 1:
        return Response("Tried to get a comment with an invalid author", status=status.HTTP_400_BAD_REQUEST)
    # add the author of the comment to the comment objects
    serializedComment["author"] = AuthorsSerializer(Authors.objects.get(id=serializedComment["author"])).data

    return serializedComment

def createFauxAuthor(request, author):
    if "id" not in author:
        return False
    authorId = author["id"]

    if "displayName" not in author:
        return False
    displayName = author["displayName"]
        
    if (displayName and displayName.strip() == "") or (authorId and authorId.strip() == ""):
        return False

    if "host" in author:
        host = author["host"]
    else:
        host = request.build_absolute_uri().split('/authors/')[0]
        
    url = host + '/authors/' + authorId
    profileImage = request.build_absolute_uri("https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg") 
    github = None

    Authors.objects.create(id=authorId, host=host, displayName=displayName, url=url, accepted=False, github=github, profileImage=profileImage)
    return True

class FrontendAppView(View):
    """
    Serves the compiled frontend entry point (only works if you have run `yarn
    build`).
    """
    index_file_path = os.path.join(os.path.realpath(__file__), 'build', 'index.html')
    def get(self, request):
        try:
            with open(self.index_file_path) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                """
                This URL is only used when you have built the production
                version of the app. Visit http://localhost:3000/ instead after
                running `yarn start` on the frontend/ directory
                """,
                status=501,
            )
class Assets(View):

    def get(self, _request, filename):
        path = os.path.join(os.path.dirname(__file__), 'static', filename)

        if os.path.isfile(path):
            with open(path, 'rb') as file:
                return HttpResponse(file.read())
        else:
            return HttpResponseNotFound()

#create a generalized object that allows for sorting based on date published
class DjangoObj:
    def __init__(self, obj, data):
        self.obj = obj
        self.date = obj.published
        self.data = data

    def __lt__(self, other):
        return self.date < other.date

    

class UserAPIs(viewsets.ViewSet):
    """ 
    Creates the user. 
    """
    #POST users/
    #adds a user to the default Django user table
    @swagger_auto_schema(
        operation_description="Create a new user when they first register",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )  
    @action(detail=True, methods=['post'])
    def createUser(self, request, format='json'):
        body = request.data

        usernameFromFrontend = body['displayName']
        usernameExists = Users.objects.filter(username = usernameFromFrontend).exists()

        if usernameExists == True:
            return Response(False, status=status.HTTP_200_OK)
        else:
            user = Users.objects.create_user(
                        id=uuidGenerator(),
                        username=body['displayName'],
                        password=body['password']
                    )
            AuthorsAPIs().createDefaultAuthor(user.id, user.username, remote_host)
            
            return Response(True, status=status.HTTP_200_OK)
        # return HttpResponse(status=200)

    """ 
    Login the user. 
    """
    @swagger_auto_schema(
        operation_description="Authenticate the user and log in.",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )  
    @action(detail=True, methods=['put'])
    def loginUser(self, request, format='json'):
        body = request.data
        username = body['username'] 
        password = body['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            payload = {
                'id': str(user.id),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response = Response()  
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'jwt': token
            }
            return response
        else:
            return Response("The username or password are incorrect.", status=status.HTTP_401_UNAUTHORIZED)
 
    @action(detail=True, methods=['post'])
    def authenticatedUser(self, request, format='json'): 
        body = request.data

        token = body["userToken"]

        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = Users.objects.get(id=payload['id'])
        except:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        data = {'id': str(user.id)}
        return Response(data)

    def check_token(self, request, authorId):
        token = request.headers["Authorization"].split()[1]
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        userId = payload["id"]
        try:
            token = request.headers["Authorization"].split()[1]
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            userId = payload["id"]
        except:
            # To show that authorization is required
            userId = -1 

        return userId != -1 and (userId == 1 or Users.objects.filter(id=userId).count() > 0)

class PostsAPIs(viewsets.ViewSet):

    #GET authors/{AUTHOR_ID/posts/{POST_ID}
    #get the public post whose id is POST_ID
    @swagger_auto_schema(
        operation_description="Fetches the post with specific postId and authorId",
        operation_summary="Fetches the post with specific postId and authorId",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'],)
    def getPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)

        postId = kwargs["postId"]
        try:
            post = Posts.objects.get(id = postId)
        except Posts.DoesNotExist:
            return Response({"No Post Exists with this ID"}, status = status.HTTP_400_BAD_REQUEST)
        serializedPost = expandPost(post)
        return Response(serializedPost, status = status.HTTP_200_OK)
            

    #GET authors/{AUTHOR_ID}/posts
    #get the public posts of this author
    @swagger_auto_schema(
        operation_description="Fetches all the public posts made by an author",
        operation_summary="Fetches all the public posts made by an author",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'])
    def getPosts(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication Required!", status=status.HTTP_401_UNAUTHORIZED)

        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )

        visibility = request.GET.get('visibility',"PUBLIC")

        if Authors.objects.filter(id=authorId).count() == 0:
            return Response({"Author does not exist"}, status=status.HTTP_404_NOT_FOUND)

        author = Authors.objects.get(id=authorId)
        if visibility == Posts.PUBLIC: posts = Posts.objects.filter(author=author, visibility=Posts.PUBLIC).order_by('-published')
        elif visibility == Posts.FRIENDS: posts = Posts.objects.filter(author=author, visibility=Posts.FRIENDS).order_by('-published')
        elif visibility == Posts.UNLISTED: posts = Posts.objects.filter(author=author, visibility=Posts.UNLISTED).order_by('-published')
        elif visibility == "ALL": posts = Posts.objects.filter(author=author).order_by('-published')
        else: return Response("Invalid Visibility", status=status.HTTP_400_BAD_REQUEST )

        outputDic = {}
        outputDic["count"] = posts.count()
        serializer = PostsSerializer(posts[(page-1)*size:page*size], many=True)
        outputDic["posts"] = serializer.data
        return Response(outputDic)


    #POST authors/{AUTHOR_ID/posts/{POST_ID}
    #update the post whose id is POST_ID (must be authenticated)
    @swagger_auto_schema(
        operation_description="Updates a post made by an author",
        operation_summary="Updates a post made by an author",
        operation_id="authors_posts_update",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='The Post ID'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='The title of the post'),
                'source': openapi.Schema(type=openapi.TYPE_STRING, description='The source of the post'),
                'origin': openapi.Schema(type=openapi.TYPE_STRING, description='The origin of the post'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='The description of the post'),
                'contentType': openapi.Schema(type=openapi.TYPE_STRING, description='The conte type of the post, can only be text/plain or text/markdown'),
                'visibility': openapi.Schema(type=openapi.TYPE_STRING, description='The visibility of the post, can only be PUBLIC or FRIENDS or UNLISTED'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='The content of the post'),
            }
        )
    )
    @action(detail=True, methods=['post'],)
    def updatePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        postId = kwargs["postId"]

        #check that postId exist
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to update non-existent post or non-public post"}, status=status.HTTP_400_BAD_REQUEST)
        post = Posts.objects.get(id=postId)
        body = request.data
        editableColumns = ["title", "description", "content"]
        edited = False
        for key, value in body.items():
            if key in editableColumns:
                setattr(post, key, value)
                edited = True
        if edited: post.save()
        return Response({"Success"}, status=status.HTTP_200_OK)

    #DELETE authors/{AUTHOR_ID/posts/{POST_ID}
    #remove the post whose id is POST_ID
    @swagger_auto_schema(
        operation_description="Deletes an author's post",
        operation_summary="Deletes an author's post",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['delete'],)
    def deletePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        postId = kwargs["postId"]
        try:
            Posts.objects.get(id = postId).delete()
        except Posts.DoesNotExist:
            return Response({"No Public Post Exists with this ID"}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"Success"}, status=status.HTTP_200_OK)

    #PUT authors/{AUTHOR_ID/posts
    #create a post where its id is POST_ID
    @swagger_auto_schema(
        operation_description="Creates a post for an author",
        operation_summary="Creates a post for an author",
        operation_id="authors_posts_create",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            required=['title','source','origin','description','contentType','visibility','content','originalAuthor','author','published'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='The title of the post'),
                'source': openapi.Schema(type=openapi.TYPE_STRING, description='The source of the post'),
                'origin': openapi.Schema(type=openapi.TYPE_STRING, description='The origin of the post'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='The description of the post'),
                'contentType': openapi.Schema(type=openapi.TYPE_STRING, description='The conte type of the post, can only be text/plain or text/markdown'),
                'visibility': openapi.Schema(type=openapi.TYPE_STRING, description='The visibility of the post, can only be PUBLIC or FRIENDS or UNLISTED'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='The content of the post'),
                'published': openapi.Schema(type=openapi.FORMAT_DATETIME, description='The publish date of the post'),
                'author': openapi.Schema(type=openapi.TYPE_STRING, description='optional author object with members "id" and "displayName"'),
                'originalAuthor': openapi.Schema(type=openapi.TYPE_STRING, description='optional original author object with members "id" and "displayName"'),
                'id': openapi.Schema(type=openapi.FORMAT_DATETIME, description='optional UUID for the post')
            }
        )
    )
    @action(detail=True, methods=['put'],)
    def createPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        body = request.data
        # check that authorId exist
        # if we don't have the poster, then try to make one
        if not Authors.objects.filter(id=authorId).count() == 1:
            if not 'author' in body:
                return Response({"Tried to make post from non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
            if not createFauxAuthor(request, body["author"]):
                return Response({"Invalid content provided in author"}, status=status.HTTP_400_BAD_REQUEST)
        # use provided id if available
        if 'id' in body:
            id = body['id']
        else:
            id = uuidGenerator()
        if not 'type' in body: body['type'] = "post"
        if not 'title' in body:
            if body['contentType'] != Posts.IMAGE: return Response({'title must be supplied for non-image posts'}, status=status.HTTP_400_BAD_REQUEST)
            else: body['title'] = ""
        if not 'source' in body: body['source'] = remote_host
        if not 'origin' in body: body['origin'] = remote_host
        if not 'description' in body:
            if body['contentType'] != Posts.IMAGE: return Response({'description must be supplied for non-image posts'}, status=status.HTTP_400_BAD_REQUEST)
            else: body['description'] = ""
        if not 'contentType' in body: return Response({'contentType must be supplied'}, status=status.HTTP_400_BAD_REQUEST)
        if not 'content' in body: return Response({'content must be supplied'}, status=status.HTTP_400_BAD_REQUEST)
        if not 'visibility' in body: return Response({'visibility must be supplied'}, status=status.HTTP_400_BAD_REQUEST)
        if (body['visibility'] != Posts.PUBLIC and body['visibility'] != Posts.FRIENDS and body['visibility'] != Posts.UNLISTED):
            return Response({'invalid post visibility, must be PUBLIC, FRIENDS or UNLISTED'}, status=status.HTTP_400_BAD_REQUEST)
        if (body['contentType'] != Posts.PLAINTEXT and body['contentType'] != Posts.MARKDOWN and body['contentType'] != Posts.IMAGE):
            return Response({'invalid post contentType, must be text/plain, text/markdown or image'})
        if not 'originalAuthor' in body: return Response({'originalAuthor must be supplied'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            originalAuthorId = body['originalAuthor']['id']
            Authors.objects.get(id = originalAuthorId)
        except Authors.DoesNotExist:
            if not createFauxAuthor(request, body['originalAuthor']):
                return Response({"Invalid content provided in originalAuthor"}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            originalAuthorId = body['originalAuthor']
            if Authors.objects.filter(id = originalAuthorId).count() == 0:
                return Response({"Tried to make post from non-existent originalAuthor"}, status=status.HTTP_400_BAD_REQUEST)

        if not 'published' in body:
            post = Posts.objects.create(
                id = id,
                type = body['type'],
                title = body['title'],
                source = body['source'],
                origin = body['origin'],
                description = body['description'],
                contentType = body['contentType'],
                content = body['content'],
                originalAuthor = Authors.objects.get(id = originalAuthorId),
                author = Authors.objects.get(id = authorId),
                visibility = body['visibility']
            )
        else:
            post = Posts.objects.create(
                id = id,
                type = body['type'],
                title = body['title'],
                source = body['source'],
                origin = body['origin'],
                description = body['description'],
                contentType = body['contentType'],
                content = body['content'],
                originalAuthor = Authors.objects.get(id = originalAuthorId),
                author = Authors.objects.get(id = authorId),
                published = body['published'],
                visibility = body['visibility']
            )

        serializer = PostsSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)

class CommentsAPIs(viewsets.ViewSet):

    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    #get the list of comments of the post whose id is POST_ID
    @swagger_auto_schema(
        operation_description="Gets Comments on a Post",
        operation_summary="Gets the comments on a Post",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'],)
    def getComments(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)

        postId = kwargs["postId"]
        # get the post the comment is for
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to get comments from non-existent post"}, status=status.HTTP_400_BAD_REQUEST)
        serializedPost = expandPost(Posts.objects.get(id=postId))
        
        data = []
        for comment in Comments.objects.filter(post_id=postId).order_by('-published'):
            data.append(expandComment(comment, serializedPost))

        return Response(data)

    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}
    #get the comment with given comment_id
    @swagger_auto_schema(
        operation_description="Gets a specific comment",
        operation_summary="Gets a specific comment",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'],)
    def getComment(self, request, *args, **kwargs):
        commentId = kwargs["commentId"]

        # get the comment
        if not Comments.objects.filter(id=commentId).count() == 1:
            return Response({"Tried to get a non-existent comment"}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comments.objects.get(id=commentId)

        # get the referred post
        serializedPost = PostsSerializer(Posts.objects.get(id=comment.post.id)).data
        serializedComment = expandComment(comment, serializedPost)

        return Response(serializedComment)

    #POST authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    #creates a comment for POST_ID
    @swagger_auto_schema(
        operation_description="creates a comment for POST_ID",
        operation_summary="creates a comment for POST_ID",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            required=['comment'],
            properties={
                'comment': openapi.Schema(type=openapi.TYPE_STRING, description='The text of the comment'),
                'author': openapi.Schema(type=openapi.TYPE_STRING, description='optional author object with members "id" and "displayName"'),
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='optional UUID for the comment'),                
            }
        )
    )
    @action(detail=True, methods=['post'],)
    def createComment(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        postId = kwargs["postId"]

        # check that authorId and postId exist
        # if we don't have the commenter, then try to make one
        # if we don't have the post, then error
        body = request.data
        if not Authors.objects.filter(id=authorId).count() ==1:
            if not 'author' in body:
                return Response({"Tried to make comment from non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
            if not createFauxAuthor(request, body["author"]):
                return Response({"Invalid content provided in author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to make comment on non-existent post"}, status=status.HTTP_400_BAD_REQUEST)

        author = Authors.objects.get(id=authorId)
        post = Posts.objects.get(id=postId)

        #check that contentType is a valid choice
        contentType = 'text/plain'
        if 'contentType' in body:
            if body['contentType'] == 'text/markdown':
                contentType = 'text/markdown'
            elif body['contentType'] != 'text/plain':
                return Response({"Failed comment creation. Invalid input for contentType."}, status=status.HTTP_400_BAD_REQUEST)

        if 'comment' in body and str(body['comment']).strip() != '':
            comment = str(body['comment']).strip()
        else:
            return Response({"Failed comment creation. Missing 'comment' column."}, status=status.HTTP_400_BAD_REQUEST)

        # use provided id if available
        if 'id' in body:
            id = body['id']
        else:
            id = uuidGenerator()

        Comments.objects.create(
            id = id,
            author = author,
            post = post,
            contentType = contentType,
            comment = comment
        )

        output = {}
        output["message"] = "Comment Created Successfully"
        output["id"] = id
        return Response(output, status=status.HTTP_200_OK)

class LikesAPIs(viewsets.ViewSet):
    #POST authors/{AUTHOR_ID}/posts/{POST_ID}/likes/{LIKER_ID}
    #like a post given a POST_ID and LIKER_ID
    @action(detail=True, methods=['post'])
    @swagger_auto_schema(
        operation_description="like a post",
        operation_summary="like a post",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties={
                'author': openapi.Schema(type=openapi.TYPE_STRING, description='optional author object with members "id" and "displayName"')              
            }
        )
    )
    def createPostLike(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        authenticated = UserAPIs().check_token(request, likerId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        postId = kwargs["postId"]
        
        # check that authorId and postId exist
        # if we don't have the liker, then try to make one
        # if we don't have the post, then error
        if request.data:
            body = request.data
        else:
            body = {}
        if Authors.objects.filter(id=likerId).count() < 1:
            if not 'author' in body:
                return Response({"Tried to make like from non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
            if not createFauxAuthor(request, body["author"]):
                return Response({"Invalid content provided in author"}, status=status.HTTP_400_BAD_REQUEST)
        if Posts.objects.filter(id=postId).count() < 1:
            return Response({"Tried to check likes on a non-existent post"}, status=status.HTTP_400_BAD_REQUEST)

        liker = Authors.objects.get(id=likerId)
        post = Posts.objects.get(id=postId)
        if Likes.objects.filter(post=post, author=liker).count() >= 1:
            return Response({"Tried to like a post you've already liked"}, status=status.HTTP_400_BAD_REQUEST)

        Likes.objects.create(
            id = uuidGenerator(),
            context = post.title,
            summary = f'{liker.displayName} liked your post',
            author = liker,
            post = post
        )

        return Response("{Like created successfully}", status=status.HTTP_200_OK )

    #POST authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes/{LIKER_ID}
    #like a comment given a COMMENT_ID and LIKER_ID
    @action(detail=True, methods=['post'])
    @swagger_auto_schema(
        operation_description="like a comment",
        operation_summary="like a comment",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties={
                'author': openapi.Schema(type=openapi.TYPE_STRING, description='optional author object with members "id" and "displayName"')              
            }
        )
    )
    def createCommentLike(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        authenticated = UserAPIs().check_token(request, likerId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        commentId = kwargs["commentId"]
        
        # check that authorId and commentId exist
        # if we don't have the liker, then try to make one
        # if we don't have the comment, then error
        if request.data:
            body = request.data
        else:
            body = {}
        if Authors.objects.filter(id=likerId).count() < 1:
            if not 'author' in body:
                return Response({"Tried to make like from non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
            if not createFauxAuthor(request, body["author"]):
                return Response({"Invalid content provided in author"}, status=status.HTTP_400_BAD_REQUEST)
        if Comments.objects.filter(id=commentId).count() < 1:
            return Response({"Tried to check likes on a non-existent comment"}, status=status.HTTP_400_BAD_REQUEST)

        liker = Authors.objects.get(id=likerId)
        comment = Comments.objects.get(id=commentId)
        if LikesComments.objects.filter(comment=comment, author=liker).count() >= 1:
            return Response({"Tried to like a comment you've already liked"}, status=status.HTTP_400_BAD_REQUEST)

        LikesComments.objects.create(
            id = uuidGenerator(),
            context = comment.comment,
            summary = f'{liker.displayName} liked your comment',
            author = liker,
            comment = comment
        )

        return Response("{Like created successfully}", status=status.HTTP_200_OK )

    #DELETE authors/{AUTHOR_ID}/posts/{POST_ID}/likes/{LIKER_ID}
    #deletes a post like given a POST_ID and a LIKER_ID
    @swagger_auto_schema(
        operation_description="deletes a post",
        operation_summary="deletes a post",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['delete'])
    def deletePostLike(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        authenticated = UserAPIs().check_token(request, likerId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        postId = kwargs["postId"]
        
        #check that authorId and postId exist
        if Authors.objects.filter(id=likerId).count() < 1:
            return Response({"Tried to delete a like of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if Posts.objects.filter(id=postId).count() < 1:
            return Response({"Tried to delete a like on a non-existent post"}, status=status.HTTP_400_BAD_REQUEST)
        liker = Authors.objects.get(id=likerId)
        post = Posts.objects.get(id=postId)

        if Likes.objects.filter(post=post, author=liker).count() < 1:
            return Response({"Tried to delete a non-existent like"}, status=status.HTTP_400_BAD_REQUEST)
        Likes.objects.filter(post=post, author=liker).delete()
        
        return Response({"Delete Like Successful"}, status=status.HTTP_200_OK)

    #DELETE authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes/{LIKER_ID}
    #deletes a comment like given a COMMENT_ID and a LIKER_ID
    @swagger_auto_schema(
        operation_description="deletes a comment",
        operation_summary="deletes a comment",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['delete'])
    def deleteCommentLike(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        authenticated = UserAPIs().check_token(request, likerId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        commentId = kwargs["commentId"]
        
        #check that authorId and postId exist
        if Authors.objects.filter(id=likerId).count() < 1:
            return Response({"Tried to delete a like of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if Comments.objects.filter(id=commentId).count() < 1:
            return Response({"Tried to delete a like on a non-existent comment"}, status=status.HTTP_400_BAD_REQUEST)
        liker = Authors.objects.get(id=likerId)
        comment = Comments.objects.get(id=commentId)

        if LikesComments.objects.filter(comment=comment, author=liker).count() < 1:
            return Response({"Tried to delete a non-existent like"}, status=status.HTTP_400_BAD_REQUEST)
        LikesComments.objects.filter(comment=comment, author=liker).delete()
        
        return Response({"Delete Like Successful"}, status=status.HTTP_200_OK)

    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/likes?page=value&size=value
    #a list of likes from other authors on AUTHOR_ID???s post POST_ID
    @swagger_auto_schema(
        operation_description="a list of likes on this post",
        operation_summary="a list of likes on this post",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'],)
    def getPostLikes(self, request, *args, **kwargs):    
        postId = kwargs["postId"]
        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )

        if Posts.objects.filter(id=postId).count() < 1:
            return Response({"Tried to get likes from a non-existent post"}, status=status.HTTP_400_BAD_REQUEST)
            
        likeObjs = []
        for like in Likes.objects.filter(post_id=postId):
            likeObjs.append(DjangoObj(like, LikesSerializer(like, many=False).data))

        likeObjs.sort()
        output = []
        for likeObjIdx in range((page-1)*size, page*size):
            if likeObjIdx >= len(likeObjs):
                break
            output.append(likeObjs[likeObjIdx].data)   
        
        return Response(output, status=status.HTTP_200_OK)

    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes?page=value&size=value
    #a list of likes from other authors on AUTHOR_ID???s post POST_ID comment COMMENT_ID
    @swagger_auto_schema(
        operation_description="a list of likes on this comment",
        operation_summary="a list of likes on this comment",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'],)
    def getCommentLikes(self, request, *args, **kwargs):
        commentId = kwargs["commentId"]
        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )

        if Comments.objects.filter(id=commentId).count() < 1:
            return Response({"Tried to get likes from a non-existent comment"}, status=status.HTTP_400_BAD_REQUEST)

        commentLikeObjs = []
        for like in LikesComments.objects.filter(comment_id=commentId):
            commentLikeObjs.append(DjangoObj(like, LikesCommentsSerializer(like, many=False).data))

        commentLikeObjs.sort()
        output = []
        for commentLikeObjIdx in range((page-1)*size, page*size):
            if commentLikeObjIdx >= len(commentLikeObjs):
                break
            output.append(commentLikeObjs[commentLikeObjIdx].data)   
        
        return Response(output, status=status.HTTP_200_OK)

class LikedAPIs(viewsets.ViewSet):
    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/like/{LIKER_ID}
    #returns true if authorId has made a like on postId, otherwise false
    @swagger_auto_schema(
        operation_description="returns true if authorId has made a like on postId, otherwise false",
        operation_summary="returns true if authorId has made a like on postId, otherwise false",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'])
    def getAuthorPostLiked(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        postId = kwargs["postId"]
        
        #check that authorId and postId exist
        if not Authors.objects.filter(id=likerId).count() == 1:
            return Response({"Tried to check likes of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to check likes on a non-existent post"}, status=status.HTTP_400_BAD_REQUEST)

        liker = Authors.objects.get(id=likerId)
        post = Posts.objects.get(id=postId)

        if Likes.objects.filter(post=post, author=liker).count() >= 1:
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_200_OK)
    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/comment/{COMMENT_ID}/like/{LIKER_ID}
    #returns true if authorId has made a like on commentId, otherwise false
    @swagger_auto_schema(
        operation_description="returns true if authorId has made a like on commentId, otherwise false",
        operation_summary="returns true if authorId has made a like on commentId, otherwise false",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'])
    def getAuthorCommentLiked(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        commentId = kwargs["commentId"]
        
        #check that authorId and postId exist
        if not Authors.objects.filter(id=likerId).count() == 1:
            return Response({"Tried to check likes of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Comments.objects.filter(id=commentId).count() == 1:
            return Response({"Tried to check likes on a non-existent comment"}, status=status.HTTP_400_BAD_REQUEST)

        liker = Authors.objects.get(id=likerId)
        comment = Comments.objects.get(id=commentId)

        if LikesComments.objects.filter(comment=comment, author=liker).count() >= 1:
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_200_OK)

    #GET authors/{AUTHOR_ID}/liked/inbox?page=value&size=value
    #list what public things AUTHOR_ID liked
    @swagger_auto_schema(
        operation_description="list what public things the author has liked",
        operation_summary="list what public things the author has liked",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'],)
    def getAuthorLiked(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )

        if not Authors.objects.filter(id=authorId).count() == 1:
            return Response({"Tried to check likes of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)

        likeObjs = []
        for like in Likes.objects.filter(author_id=authorId):
            likeObjs.append(DjangoObj(like, LikesSerializer(like, many=False).data))
        for commentLike in LikesComments.objects.filter(author_id=authorId):
            likeObjs.append(DjangoObj(commentLike, LikesCommentsSerializer(commentLike, many=False).data))

        likeObjs.sort()
        output = []
        for likeObjIdx in range((page-1)*size, page*size):
            if likeObjIdx >= len(likeObjs):
                break
            output.append(likeObjs[likeObjIdx].data)   
        
        return Response(output, status=status.HTTP_200_OK)


class InboxAPIs(viewsets.ViewSet):

    #GET authors/{AUTHOR_ID}/inbox?page=value&size=value
    #if authenticated get a list of posts sent to AUTHOR_ID (paginated)
    @swagger_auto_schema(
        operation_description="get a list of posts/likes/comments sent to author (paginated)",
        operation_summary="get a list of posts/likes/comments sent to author (paginated)",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'],)
    def getInbox(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )

        if not Authors.objects.filter(id=authorId).count() == 1:
            return Response({"Tried to check inbox of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)

        inboxObjs = []
        #get enough posts, sorted
        oldestDate = None
        for inbox in Inbox.objects.filter(author_id=authorId):
            post = Posts.objects.get(id=inbox.post_id)
            inboxObjs.append(DjangoObj(post, PostsSerializer(post, many=False).data))
            if not oldestDate or post.published < oldestDate:
                oldestDate = post.published

        # only include objects that were published after the oldest publish date of a post
        for post in Posts.objects.filter(author_id=authorId):
            #get enough likes, sorted
            for like in Likes.objects.filter(post_id=post.id):
                if like.published >= oldestDate:
                    inboxObjs.append(DjangoObj(like, LikesSerializer(like, many=False).data))

            #get enough comments, sorted
            for comment in Comments.objects.filter(post_id=post.id):
                if comment.published >= oldestDate:
                    inboxObjs.append(DjangoObj(comment, CommentsSerializer(comment, many=False).data))

        # enough comment likes, sorted
        for myComment in Comments.objects.filter(author_id=authorId):
            for commentLike in LikesComments.objects.filter(comment_id=myComment.id):
                if commentLike.published >= oldestDate:
                    inboxObjs.append(DjangoObj(commentLike, LikesCommentsSerializer(commentLike, many=False).data))

        #paginate
        inboxObjs.sort()
        outputDic = {}
        outputDic["inbox"] = []
        outputDic["count"] = len(inboxObjs)
        for inboxObjIdx in range((page-1)*size, page*size):
            if inboxObjIdx >= outputDic["count"]:
                break
            outputDic["inbox"].append(inboxObjs[inboxObjIdx].data)       

        if outputDic["count"] == 0:
            return Response("{Nothing to show}", status=status.HTTP_200_OK )

        return Response(outputDic, status=status.HTTP_200_OK)

    #*POST authors/{AUTHOR_ID}/inbox + /{POST_ID}
    #send a post to the author
    @swagger_auto_schema(
        operation_description="send a post to the author",
        operation_summary="send a post to the author",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['post'])
    def sendPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]

        #check that authorId and postId exist
        if not Authors.objects.filter(id=authorId).count() ==1:
            return Response({"Tried to send post to non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to send non-existent post"}, status=status.HTTP_400_BAD_REQUEST)

        author = Authors.objects.get(id=authorId)
        post = Posts.objects.get(id=postId)
        Inbox.objects.create(
            id = uuidGenerator(),
            author = author,
            post = post
        )

        return Response({"Post Sent to Inbox Successfully"}, status=status.HTTP_200_OK)

    #*POST inbox/public/{AUTHOR_ID}/{POST_ID}
    #send a post to the people following this author
    @swagger_auto_schema(
        operation_description="send a post to the people following this author",
        operation_summary="send a post to the people following this author",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['post'])
    def sendPublicPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        postId = kwargs["postId"]

        #check that authorId and postId exist
        if not Authors.objects.filter(id=authorId).count() ==1:
            return Response({"Tried to send post as a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to send non-existent post"}, status=status.HTTP_400_BAD_REQUEST)
        author = Authors.objects.get(id=authorId)
        post = Posts.objects.get(id=postId)

        #find all followers and add post to inbox
        toCreate = []
        numFollowers = 0
        for follower in Followers.objects.filter(followed=author):
            numFollowers += 1
            followerAuthor = Authors.objects.get(id=follower.follower.id)
            toCreate.append(Inbox(
                id=uuidGenerator(),
                author = followerAuthor,
                post = post
            ))
        Inbox.objects.bulk_create(toCreate)
        string = f'Successfully sent post to your {numFollowers} followers'
        return Response({string}, status=status.HTTP_200_OK)


    #*POST inbox/friend/{AUTHOR_ID}/{POST_ID}
    #send a post to this author's friends
    @swagger_auto_schema(
        operation_description="send a post to this author's friends",
        operation_summary="send a post to this author's friends",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['post'])
    def sendFriendPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        postId = kwargs["postId"]

        #check that authorId and postId exist
        if not Authors.objects.filter(id=authorId).count() ==1:
            return Response({"Tried to send post as a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to send non-existent post"}, status=status.HTTP_400_BAD_REQUEST)
        author = Authors.objects.get(id=authorId)
        post = Posts.objects.get(id=postId)

        #find all followers, check if author follows them too, then add post to inbox
        toCreate = []
        numFriends = 0
        for follower in Followers.objects.filter(followed=author):
            followerAuthor = Authors.objects.get(id=follower.follower.id)
            if Followers.objects.filter(followed=followerAuthor, follower=author).count() >= 1:
                numFriends += 1
                toCreate.append(Inbox(
                    id=uuidGenerator(),
                    author = followerAuthor,
                    post = post
                ))

        Inbox.objects.bulk_create(toCreate)
        string = f'Successfully sent post to your {numFriends} friends'
        return Response({string}, status=status.HTTP_200_OK)

    #*DELETE authors/{AUTHOR_ID}/inbox
    #clear the inbox
    @swagger_auto_schema(
        operation_description="clear the inbox",
        operation_summary="clear the inbox",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['delete'],)
    def deleteInbox(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        if not Authors.objects.filter(id=authorId).count() == 1:
            return Response({"Tried to delete inbox on non-existent author"}, status=status.HTTP_400_BAD_REQUEST)

        authorObj = Authors.objects.get(id=authorId)
        Inbox.objects.filter(author=authorObj).delete()
        
        return Response({"Delete Inbox Successful"}, status=status.HTTP_200_OK)

class FollowRequestsAPIs(viewsets.ViewSet):

    #GET authors/{AUTHOR_ID}/followRequest
    #get all the people who want to follow AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Fetches all follow requests with a specific author_id",
        operation_summary="Fetches all follow requests with a specific author_id",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'],)
    def getFollowRequests(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            requestFollowers = FollowRequests.objects.filter(receiver=authorId)
        except FollowRequests.DoesNotExist:
            requestFollowers = None
        serializer = FollowRequestsSerializer(requestFollowers, many=True)
        return Response(serializer.data)

    #DELETE authors/{AUTHOR_ID}/followRequest/{FOREIGN_AUTHOR_ID}
    #remove FOREIGN_AUTHOR_ID's request to follow AUTHOR_ID (when AUTHOR_ID approve/deny a request)
    @swagger_auto_schema(
        operation_description="Delete a follow request with a specific author_id and foreign_author_id",
        operation_summary="Delete a follow request with a specific author_id and foreign_author_id",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )    
    @action(detail=True, methods=['delete'],)
    def removeRequest(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        foreignAuthorId = kwargs["foreignAuthorId"]
        try:
            requestFollowers = FollowRequests.objects.get(receiver=authorId, requester=foreignAuthorId)
            requestFollowers.delete()
        except FollowRequests.DoesNotExist:
            requestFollowers = None
        serializer = FollowRequestsSerializer(requestFollowers)
        return Response(serializer.data)

    #GET authors/{AUTHOR_ID}/followRequest/{FOREIGN_AUTHOR_ID}
    #check if FOREIGN_AUTHOR_ID has requested to follow AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Fetches a follow request with a specific author_id and foreign_author_id",
        operation_summary="Fetches a follow request with a specific author_id and foreign_author_id",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )   
    @action(detail=True, methods=['get'],)
    def checkRequestedToFollow(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]

        authenticated = UserAPIs().check_token(request, foreignAuthorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
        try:
            followRequested = FollowRequests.objects.get(receiver=authorId, requester=foreignAuthorId)
        except FollowRequests.DoesNotExist:
            followRequested = None
        serializer = FollowRequestsSerializer(followRequested)
        return Response(serializer.data)

    #POST authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #create AUTHOR_ID request to follow FOREIGN_AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Adds a follow request with a specific author_id and foreign_author_id",
        operation_summary="Adds a follow request with a specific author_id and foreign_author_id",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties={
                'author': openapi.Schema(type=openapi.TYPE_STRING, description='optional author object with members "id" and "displayName"'),
                'foreignAuthor': openapi.Schema(type=openapi.TYPE_STRING, description='optional foreignAuthor object with members "id" and "displayName"')        
            }
        )
    )  
    @action(detail=True, methods=['post'],)
    def requestToFollow(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        foreignAuthorId = kwargs["foreignAuthorId"]
        if request.data:
            body = request.data
        else:
            body = {}

        # check that authorId exist
        # if we don't have the follower, then try to make one
        if not Authors.objects.filter(id=authorId).count() ==1:
            if not 'author' in body:
                return Response({"Tried to make follow as a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
            if not createFauxAuthor(request, body["author"]):
                return Response({"Invalid content provided in author"}, status=status.HTTP_400_BAD_REQUEST)

        # check that foreignAuthorId exist
        # if we don't have the followee, then try to make one
        if not Authors.objects.filter(id=foreignAuthorId).count() ==1:
            if not 'foreignAuthor' in body:
                return Response({"Tried to follow a a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
            if not createFauxAuthor(request, body["foreignAuthor"]):
                return Response({"Invalid content provided in foreignAuthor"}, status=status.HTTP_400_BAD_REQUEST)

        # check that follow request doesn't already exist
        if not FollowRequests.objects.filter(requester=authorId, receiver=foreignAuthorId).count() == 0:
            return Response({"Failed to send a request to follow as a request to follow already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # check that follow relationship doesn't already exist
        if not Followers.objects.filter(follower=authorId, followed=foreignAuthorId).count() == 0:
            return Response({"Failed to send a request to follow as you are already following"}, status=status.HTTP_400_BAD_REQUEST)
        
        FollowRequests.objects.create(
            id = uuidGenerator(),
            requester = Authors.objects.get(id = authorId),
            receiver = Authors.objects.get(id = foreignAuthorId)
        )
        return Response({"Request to follow Successful"}, status=status.HTTP_200_OK)
    
class FollowsAPIs(viewsets.ViewSet):

    #GET authors/{AUTHOR_ID}/followers
    #get all the followers of AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Fetches all the followers of a specific author_id",
        operation_summary="Fetches all the followers of a specific author_id",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )  
    @action(detail=True, methods=['get'],)
    def getFollowers(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            followers = Followers.objects.filter(followed=authorId)
        except Followers.DoesNotExist:
            followers = None
        serializer = FollowersSerializer(followers, many=True)

        # get the host of each follower
        for i in range(len(serializer.data)):
            serializer.data[i]["followerObj"] = AuthorsSerializer(Authors.objects.get(id = serializer.data[i]["follower"])).data
            serializer.data[i]["followedObj"] = AuthorsSerializer(Authors.objects.get(id = serializer.data[i]["followed"])).data

        return Response(serializer.data)

    #GET authors/{AUTHOR_ID}/friends
    #get all the friends of AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Fetches all the friends of a specific author_id",
        operation_summary="Fetches all the friends of a specific author_id",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )  
    @action(detail=True, methods=['get'],)
    def getFriends(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)

        friends = []
        for follower in Followers.objects.filter(followed=authorId):
            if Followers.objects.filter(followed=follower.follower, follower=authorId).count() > 0:
                friendSerialized = FollowersSerializer(follower, many=False).data
                friendSerialized["followerObj"] = AuthorsSerializer(Authors.objects.get(id = follower.follower.id)).data
                friendSerialized["followedObj"] = AuthorsSerializer(Authors.objects.get(id = follower.followed.id)).data
                friends.append(friendSerialized)
        
        return Response(friends)
    
    #GET authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #check if FOREIGN_AUTHOR_ID is following AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Fetches a follow relationship object with a specific author_id and foreign_author_id",
        operation_summary="Fetches a follow relationship object with a specific author_id and foreign_author_id",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )  
    @action(detail=True, methods=['get'],)
    def checkFollower(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]

        authenticated = UserAPIs().check_token(request, foreignAuthorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
        try:
            follower = Followers.objects.get(followed=authorId, follower=foreignAuthorId)
        except Followers.DoesNotExist:
            follower = None
        serializer = FollowersSerializer(follower)
        return Response(serializer.data)

    #PUT authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Adds a follow relationship object with a specific author_id and foreign_author_id",
        operation_summary="Adds a follow relationship object with a specific author_id and foreign_author_id",
        operation_id="authors_followers_create",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )  
    @action(detail=True, methods=['put'],)
    def addFollower(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        foreignAuthorId = kwargs["foreignAuthorId"]
        if not FollowRequests.objects.filter(receiver=authorId, requester=foreignAuthorId).count() == 1:
            return Response({"Failed to add a follower. The other party hasn't requested to follow you"}, status=status.HTTP_400_BAD_REQUEST)
        Followers.objects.create(
            id = uuidGenerator(),
            followed = Authors.objects.get(id = authorId),
            follower = Authors.objects.get(id = foreignAuthorId)
        )

        FollowRequests.objects.get(receiver=authorId, requester=foreignAuthorId).delete()
        return Response({"Add a follower Successful"}, status=status.HTTP_200_OK)

    #DELETE authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Deletes a follow relationship object with a specific author_id and foreign_author_id",
        operation_summary="Deletes a follow relationship object with a specific author_id and foreign_author_id",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        }
    )  
    @action(detail=True, methods=['delete'],)
    def removeFollower(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        authenticated = UserAPIs().check_token(request, foreignAuthorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            follower = Followers.objects.get(followed=authorId, follower=foreignAuthorId)
            follower.delete()
        except Followers.DoesNotExist:
            return Response({"Failed to remove follower. You need to follow them first before you can unfollow them"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Remove follower Successful"}, status=status.HTTP_200_OK)
    
    #POST authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #create FOREIGN_AUTHOR_ID's request to follow AUTHOR_ID
    @swagger_auto_schema(
        operation_description="Adds a follow request with a specific author_id and foreign_author_id",
        operation_summary="Adds a follow request with a specific author_id and foreign_author_id",
        operation_id="authors_followers_update",
        responses={
            "200": "Success",
            "4XX": "Bad Request"
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties={
                'author': openapi.Schema(type=openapi.TYPE_STRING, description='optional author object with members "id" and "displayName"')              
            }
        )
    )  
    @action(detail=True, methods=['post'],)
    def requestToFollow(self, request, *args, **kwargs):
        return FollowRequestsAPIs.requestToFollow(self, request, *args, **kwargs)

class AuthorsAPIs(viewsets.ViewSet):

    # This image is licensed under Adobe Standard License
    generic_profile_image_path = "https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg"

    #TESTED
    #GET //service/authors/{AUTHOR_ID}
    @swagger_auto_schema(
        operation_description="Fetches the author with id authorId.",
        operation_summary="Fetches the author with id authorId.",
        responses={
            "200": "Success",
            "404": "Author with id authorId does not exist in database"
        }
    )
    @action(detail=True, methods=['get'])
    def getAuthor(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]

        author = Authors.objects.filter(id=authorId)
        # Since id is the primary key of the Author table, there can only be 0 ot
        # 1 authors with this id
        if author.count() == 0:
            return Response("Author does not exist", status=status.HTTP_204_NO_CONTENT)
        
        author = author.get(id=authorId)

        serializer = AuthorsSerializer(author, many=False)
        return Response(serializer.data)
    
    #TESTED
    #GET //service/find?query={SEARCH_QUERY}&page={PAGE_NUM}&size={PAGE_SIZE}
    @swagger_auto_schema(
        operation_description="Fetches a page of authors whose displayName contains the value of the \"query\" query parameter.",
        operation_summary="Fetches authors whose displayName contains the value of the \"query\" query parameter.",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY,
                        "The query parameter.",
                        type=openapi.TYPE_INTEGER),
            openapi.Parameter('page', openapi.IN_QUERY,
                      "The page number required.",
                      type=openapi.TYPE_INTEGER
                      ),
            openapi.Parameter('size', openapi.IN_QUERY,
                      "The size of each page.",
                      type=openapi.TYPE_INTEGER
                      )
        ],
        responses= {
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    @action(detail=True, methods=['get'])
    def searchForAuthors(self, request, *args, **kwargs):
        #We search for displayName matching search_query
        search_query = request.GET.get('query')
        page_num = request.GET.get('page', 1)
        page_size = request.GET.get('size', 10)

        authors = Authors.objects.filter(displayName__icontains=search_query, host=remote_host)
        paginator = Paginator(authors, page_size)
        page_obj = paginator.get_page(page_num)
        serializer = AuthorsSerializer(page_obj, many=True)

        res = {
            "numPages": f"{paginator.num_pages}",
            "authorsPage": serializer.data
        }

        return Response(res, content_type="application/json")

    @swagger_auto_schema(
        operation_description="Fetches a page of authors.",
        operation_summary="Fetches a page of authors.",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY,
                      "The page number required.",
                      type=openapi.TYPE_INTEGER),
            openapi.Parameter('size', openapi.IN_QUERY,
                      "The size of each page.",
                      type=openapi.TYPE_INTEGER)
        ],
        responses= {
            "200": "Success",
            "4XX": "Bad Request"
        }
    )
    #TESTED
    #GET //service/authors?page={PAGE_NUM}&size={PAGE_SIZE}
    @action(detail=True, methods=['get'])
    def getAuthors(self, request, *args, **kwargs):
        page_num = request.GET.get('page', 1)
        page_size = request.GET.get('size', 10)

        authors = Authors.objects.filter(host=remote_host)
        paginator = Paginator(authors, page_size)
        page_obj = paginator.get_page(page_num)
        serializer = AuthorsSerializer(page_obj, many=True)

        res = {
            "numPages": f"{paginator.num_pages}",
            "authorsPage": serializer.data
        }

        return Response(res, content_type="application/json")

    #TESTED
    #POST //service/authors/{AUTHOR_ID}
    @swagger_auto_schema(
        operation_description="Modifies either the github or profileImage attributes of an author with id authorId or both.",
        operation_summary="Modifies either the github or profileImage attributes of an author with id authorId or both.",
        operation_id="authors_update",
        responses={
            "204": "No Content. Author was modified successfully.",
            "400": "Bad Request",
            "404": "Author with id authorId does not exist in database"
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            required=[],
            properties={
                'github': openapi.Schema(type=openapi.TYPE_STRING, description='The new Github URL of the author.'),
                'profileimage': openapi.Schema(type=openapi.TYPE_STRING, description='The new profile image URL of the author.'),
            }
        )
    )
    @action(detail=True, methods=['post'])
    def modifyAuthor(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        authenticated = UserAPIs().check_token(request, authorId)
        if not authenticated:
            return Response("Authentication required!", status=status.HTTP_401_UNAUTHORIZED)

        author = Authors.objects.filter(id=authorId)
        # Since id is the primary key of the Author table, there can only be 0 ot
        # 1 authors with this id
        if author.count() == 0:
            return Response("Author does not exist!", status=status.HTTP_404_NOT_FOUND)
        author = author.get(id=authorId)

        request_body = request.data
        if type(request_body) != dict:
            return Response("Send JSON data!", status=status.HTTP_400_BAD_REQUEST)

        editable_fields = ["github", "profileImage"]
        for field in request_body.keys():
            if field not in editable_fields:
                return Response(f"You are not allowed to modify field {field} or {field} does not exist!", status=status.HTTP_400_BAD_REQUEST)
        
        for field, value in request_body.items():
            if field == "profileImage":
                if value.strip() == "":
                    value = request.build_absolute_uri(self.generic_profile_image_path)
            if field == "github" and value.strip() == "":
                value = None
            setattr(author, field, value)

        author.save()

        return Response("Modified Author successfully", status=status.HTTP_204_NO_CONTENT)
        #else:
        #    return Response("Authentication Required", status=status.HTTP_401_UNAUTHORIZED)
    
    #TESTED
    #PUT //service/authors
    @swagger_auto_schema(
        operation_description="Creates an author with a certain displayName. This is meant to be used only after someone registers, as a unique ID will be generated then.",
        operation_summary="Creates an author with a certain displayName.",
        operation_id="authors_create",
        responses={
            "201": "Created author successfully",
            "400": "Bad Request",
            "404": "Author with id authorId does not exist in database",
            "409": "Conflict. An author already exists with either the id or the displayName specified in the request."
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            required=["authorId", "displayName"],
            properties={
                'authorId': openapi.Schema(type=openapi.TYPE_STRING, description='The ID of the author to be created.'),
                'displayName': openapi.Schema(type=openapi.TYPE_STRING, description='The displayName of the author to be created.'),
            }
        )
    )
    @action(detail=True, methods=['put'])
    def createAuthor(self, request, *args, **kwargs):

        request_body = request.data
        if type(request_body) != dict:
            return Response("Send JSON data!", status=status.HTTP_400_BAD_REQUEST)
        
        if "displayName" in request_body and request_body["displayName"].strip() != "" \
          and "authorId" in request_body and request_body["authorId"].strip() != "":
            authorId = request_body['authorId']
            displayName = request_body['displayName']
            authorByDisplayName = Authors.objects.filter(displayName=displayName)
            if authorByDisplayName.count() == 1:
                return Response("Display name already exists!", status=status.HTTP_409_CONFLICT)
            authorById = Authors.objects.filter(id=authorId)
            if authorById.count() == 1:
                return Response("Id already exists!", status=status.HTTP_409_CONFLICT) 
        else:
            return Response("Can't create a profile with no display name!", status=status.HTTP_400_BAD_REQUEST)
        
        self.createDefaultAuthor(authorId, displayName, remote_host)

        return Response("Created Author successfully", status=status.HTTP_201_CREATED)

    def createDefaultAuthor(self, authorId, displayName, host):
        url = host + '/authors/' + authorId

        author = Authors.objects.create(id=authorId, host=host, displayName=displayName, url=url, accepted=False, github=None, profileImage=self.generic_profile_image_path)

        author.save()


class ImagesAPIs(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="Uploads an image encoded as base64 to the database. The image will correspond to referenceId, which" \
            "is either an authorId (so the image is a profileImage) or a postId (so the image is a post).",
        operation_summary="Uploads an image encoded as base64 to the database.",
        operation_id="image_upload",
        responses={
            "201": "New image was uploaded successfully. A new URI was created for this image.",
            "204": "Image was modified successfully. The image data at an existing URI was updated.",
            "400": "Bad Request."
        },
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            required=["imageContent"],
            properties={
                'imageContent': openapi.Schema(type=openapi.TYPE_STRING, description='The string corresponding to the base64 encoded image.'),
            }
        )
    )
    #POST //service/images/{REFERENCE_ID}
    @action(detail=True, methods=['post'])
    def uploadImage(self, request, *args, **kwargs):

        referenceId = kwargs["referenceId"]
        image_base64 = base64.b64encode(request.body)
        try:
            image_record = Images.objects.get(referenceId=referenceId)
            update = True
        except database.models.Images.DoesNotExist:
            update = False
        
        if update:
            image_record.imageContent = image_base64
        else:
            image_record = Images.objects.create(id=uuidGenerator(), imageContent=image_base64, referenceId=referenceId)
        
        image_record.save()

        if update:
            return Response("Image Uploaded", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Image Uploaded", status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_description="Fetches the image (as binary data NOT base64) corresponding to referenceId. referenceId could either be an authorId or a postId. " \
            "If referenceId is an authorId, the the image is a profileImage. If referenceId is a postId, then the image is a post.",
        operation_summary="Fetches the image (as binary data NOT base64) corresponding to referenceId. ReferenceId could either be an authorId or a postId.",
        responses= {
            "200": "Success",
            "404": "Image corresponding to imageId was not found."
        }
    )
    #GET //service/images/{REFERENCE_ID}
    @action(detail=True, method=['get'])
    def getImage(self, request, *args, **kwargs):
        referenceId = kwargs["referenceId"]
        image_record = Images.objects.filter(referenceId=referenceId)
        if image_record.count() == 0:
            return Response("Image not found!", status=status.HTTP_404_NOT_FOUND)
        else:
            image_record = image_record.get(referenceId=referenceId)

            # The image is stored as base64 in the database. This converts it back into binary data before sending it back.
            image_content_b64 = image_record.imageContent
            image_content = bytes(base64.b64decode(image_content_b64))

            # https://stackoverflow.com/a/53888054
            response = HttpResponse(image_content, content_type="image/*")
            response['Content-Disposition'] = 'inline"'
            return response
        

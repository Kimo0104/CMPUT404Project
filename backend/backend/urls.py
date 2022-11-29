"""backend URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from database.views import AuthorsAPIs, PostsAPIs, CommentsAPIs, LikesAPIs, LikedAPIs, InboxAPIs, FollowRequestsAPIs, FollowsAPIs, UserAPIs, ImagesAPIs
from rest_framework import permissions
from django.views.generic import TemplateView

# https://www.jasonmars.org/2020/04/22/add-swagger-to-django-rest-api-quickly-4-mins-without-hiccups/
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Social Distribution API",
        default_version='v1',
        description="Welcome to the world of Social Distribution",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #swagger docs. Go to /doc for swagger and /redoc for redoc view
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    # authentication
    path('users', UserAPIs.as_view({
        "post": "createUser",
        "put": "loginUser",
    }), name = 'users'),

    path('users/auth', UserAPIs.as_view({
        "post": "authenticatedUser",
    }), name = 'auth'),

    path('admin/', admin.site.urls, name = 'admin'),

    #posts
    path('authors/<str:authorId>/posts', PostsAPIs.as_view({"put": "createPost", "get": "getPublicPosts"}), name = 'post'),
    path('authors/<str:authorId>/posts/<str:postId>', PostsAPIs.as_view({
        "get": "getPost",
        "post": "updatePost",
        "delete": "deletePost"
    }), name = 'existing-post'),
    path('authors/<str:authorId>/posts/<str:postId>/image', PostsAPIs.as_view({"get": "getImagePost"}), name = 'image-post'),

    #comments
    path('authors/<str:authorId>/posts/<str:postId>/comments', CommentsAPIs.as_view({
        "get": "getComments",
        "post": "createComment"
    }), name = 'comments'),
    path('authors/<str:authorId>/posts/<str:postId>/comments/<str:commentId>', CommentsAPIs.as_view({"get": "getComment"}), name = 'comment'),


    #likes
    path('authors/<str:authorId>/posts/<str:postId>/likes', LikesAPIs.as_view({"get": "getPostLikes"}), name = 'get-post-like'),
    path('authors/<str:authorId>/posts/<str:postId>/likes/<str:likerId>', LikesAPIs.as_view({"post": "createPostLike", "delete": "deletePostLike"}), name = 'post-like'),
    path('authors/<str:authorId>/posts/<str:postId>/comments/<str:commentId>/likes', LikesAPIs.as_view({"get": "getCommentLikes"}), name = 'get-comment-like'),
    path('authors/<str:authorId>/posts/<str:postId>/comments/<str:commentId>/likes/<str:likerId>', LikesAPIs.as_view({"post": "createCommentLike", "delete": "deleteCommentLike"}), name = 'comment-like'),

    #liked
    path('authors/<str:authorId>/liked', LikedAPIs.as_view({"get": "getAuthorLiked"}), name = 'liked'),
    path('authors/<str:authorId>/posts/<str:postId>/liked/<str:likerId>', LikedAPIs.as_view({"get": "getAuthorPostLiked"}), name = 'has-liked'),
    path('authors/<str:authorId>/posts/<str:postId>/comments/<str:commentId>/liked/<str:likerId>', LikedAPIs.as_view({"get": "getAuthorCommentLiked"}), name = 'has-liked-comment'),

    #inbox
    path('authors/<str:authorId>/inbox', InboxAPIs.as_view({
        "get": "getInbox",
        "delete": "deleteInbox"
    }), name = 'inbox'),
    path('inbox/public/<str:authorId>/<str:postId>', InboxAPIs.as_view({"post": "sendPublicPost"}), name = 'send-public-inbox'),
    path('inbox/friend/<str:authorId>/<str:postId>', InboxAPIs.as_view({"post": "sendFriendPost"}), name = 'send-friend-inbox'),
    path('authors/<str:authorId>/inbox/<str:postId>', InboxAPIs.as_view({"post": "sendPost"}), name = 'send-direct-inbox'),

    #followRequests
    path('authors/<str:authorId>/followRequest', FollowRequestsAPIs.as_view({"get": "getFollowRequests"}), name = 'get-follow-requests'),
    path('authors/<str:authorId>/followRequest/<str:foreignAuthorId>', FollowRequestsAPIs.as_view({
        "delete": "removeRequest",
        "get": "checkRequestedToFollow"}), name = 'manage-follow-requests'),
    # path('authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowRequestsAPIs.as_view({"post": "requestToFollow"})),

    #follows
    path('authors/<str:authorId>/followers', FollowsAPIs.as_view({"get": "getFollowers"}), name = 'get-followers'),
    path('authors/<str:authorId>/friends', FollowsAPIs.as_view({"get": "getFriends"}), name = 'get-friends'),
    path('authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowsAPIs.as_view({
        "get": "checkFollower",
        "put": "addFollower",
        "delete": "removeFollower",
        "post": "requestToFollow"}), name = 'manage-followers'),

    #authors
    path('authors', AuthorsAPIs.as_view({"get":"getAuthors", "put":"createAuthor"}), name = 'authors'),
    path('authors/<str:authorId>', AuthorsAPIs.as_view({"get":"getAuthor", "post":"modifyAuthor"}), name = 'manage-authors'),
    path('find', AuthorsAPIs.as_view({"get":"searchForAuthors"}), name = 'find-authors'),

    #images
    #path('images/<str:authorId>', ImagesAPIs.as_view({"put":"putImage", "get":"getImage"}), name = 'images')
    path('images/<str:referenceId>', ImagesAPIs.as_view({"post":"uploadImage", "get":"getImage"})),
    
    #heroku
    re_path('.*', TemplateView.as_view(template_name='index.html')),
]


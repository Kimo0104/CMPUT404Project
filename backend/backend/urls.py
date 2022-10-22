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
from django.urls import path
from database.views import PostsAPIs, CommentsAPIs, LikesAPIs, LikedAPIs, InboxAPIs, FollowRequestsAPIs, FollowsAPIs

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),

    #posts
    path('service/authors/<str:authorId>/posts/<str:postId>', PostsAPIs.as_view({
        "get": "getPost",
        "post": "updatePost",
        "delete": "deletePost",
        "create": "createPost"
    })),
    path('service/authors/<str:authorId>/posts/<str:postId>/image', PostsAPIs.as_view({"get": "getImagePost"})),

    #comments
    path('service/authors/<str:authorId>/posts/<str:postId>/comments', CommentsAPIs.as_view({
        "get": "getComments",
        "post": "createComment"
    })),


    #likes
    path('service/authors/<str:authorId>/posts/<str:postId>/likes', LikesAPIs.as_view({"get": "getPostLikes"})),
    path('service/authors/<str:authorId>/posts/<str:postId>/comments/<str:commentId>/likes', LikesAPIs.as_view({"get": "getCommentLikes"})),

    #liked
    path('service/authors/<str:authorId>/likes', LikedAPIs.as_view({"get": "getAuthorLiked"})),

    #inbox
    path('service/authors/<str:authorId>/inbox', InboxAPIs.as_view({
        "get": "getInbox",
        "post": "sendPost",
        "delete": "deleteInbox"
    })),

    #followRequests
    path('service/authors/<str:authorId>/followRequest', FollowRequestsAPIs.as_view({"get", "getFollowRequests"})),
    path('service/authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowRequestsAPIs.as_view({"delete", "removeRequest"})),
    path('service/authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowRequestsAPIs.as_view({"post", "requestToFollow"})),

    #follows
    path('service/authors/<str:authorId>/followers', FollowsAPIs.as_view({"get", "getFollowers"})),
    path('service/authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowsAPIs.as_view({"get", "checkFollower"})),
    path('service/authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowsAPIs.as_view({"put", "addFollower"})),
    path('service/authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowsAPIs.as_view({"delete", "removeFollower"}))
]

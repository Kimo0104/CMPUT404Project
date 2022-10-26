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
from database.views import AuthorsAPIs, PostsAPIs, CommentsAPIs, LikesAPIs, LikedAPIs, InboxAPIs, FollowRequestsAPIs, FollowsAPIs

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),

    #posts
    path('authors/<str:authorId>/posts/<str:postId>', PostsAPIs.as_view({
        "get": "getPost",
        "post": "updatePost",
        "delete": "deletePost",
        "put": "createPost"
    })),
    path('authors/<str:authorId>/posts/<str:postId>/image', PostsAPIs.as_view({"get": "getImagePost"})),

    #comments
    path('authors/<str:authorId>/posts/<str:postId>/comments', CommentsAPIs.as_view({
        "get": "getComments",
        "post": "createComment"
    })),


    #likes
    path('authors/<str:authorId>/posts/<str:postId>/likes', LikesAPIs.as_view({"get": "getPostLikes"})),
    path('authors/<str:authorId>/posts/<str:postId>/likes/<str:likerId>', LikesAPIs.as_view({"post": "createPostLike", "delete": "deletePostLike"})),
    path('authors/<str:authorId>/posts/<str:postId>/comments/<str:commentId>/likes', LikesAPIs.as_view({"get": "getCommentLikes"})),

    #liked
    path('authors/<str:authorId>/liked', LikedAPIs.as_view({"get": "getAuthorLiked"})),
    path('authors/<str:authorId>/posts/<str:postId>/liked/<str:likerId>', LikedAPIs.as_view({"get": "getAuthorPostLiked"})),

    #inbox
    path('authors/<str:authorId>/inbox', InboxAPIs.as_view({
        "get": "getInbox",
        "delete": "deleteInbox"
    })),
    path('authors/<str:authorId>/inbox/<str:postId>', InboxAPIs.as_view({"post": "sendPost"})),

    #followRequests
    path('authors/<str:authorId>/followRequest', FollowRequestsAPIs.as_view({"get": "getFollowRequests"})),
    path('authors/<str:authorId>/followRequest/<str:foreignAuthorId>', FollowRequestsAPIs.as_view({"delete": "removeRequest"})),
    # path('authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowRequestsAPIs.as_view({"post": "requestToFollow"})),

    #follows
    path('authors/<str:authorId>/followers', FollowsAPIs.as_view({"get": "getFollowers"})),
    path('authors/<str:authorId>/followers/<str:foreignAuthorId>', FollowsAPIs.as_view({
        "get": "checkFollower",
        "put": "addFollower",
        "delete": "removeFollower",
        "post": "requestToFollow"})),


    #authors
    path('authors', AuthorsAPIs.as_view({"get":"getAuthors", "put":"createAuthor"})),
    path('authors/<str:authorId>', AuthorsAPIs.as_view({"get":"getAuthor", "post":"modifyAuthor"})),
    path('find', AuthorsAPIs.as_view({"get":"searchForAuthors"})),


]

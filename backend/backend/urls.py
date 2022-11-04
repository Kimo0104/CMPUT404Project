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
from database.views import AuthorsAPIs, PostsAPIs, CommentsAPIs, LikesAPIs, LikedAPIs, InboxAPIs, FollowRequestsAPIs, FollowsAPIs, UserAPIs, ImagesAPIs
from rest_framework import permissions

# https://www.jasonmars.org/2020/04/22/add-swagger-to-django-rest-api-quickly-4-mins-without-hiccups/
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Jaseci API",
        default_version='v1',
        description="Welcome to the world of Jaseci",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
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
    })),

    path('admin/', admin.site.urls),

    #posts
    path('authors/<str:authorId>/posts', PostsAPIs.as_view({"put": "createPost", "get": "getPublicPosts"})),
    path('authors/<str:authorId>/posts/<str:postId>', PostsAPIs.as_view({
        "get": "getPost",
        "post": "updatePost",
        "delete": "deletePost"
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
    path('authors/<str:authorId>/posts/<str:postId>/comments/<str:commentId>/likes/<str:likerId>', LikesAPIs.as_view({"post": "createCommentLike", "delete": "deleteCommentLike"})),

    #liked
    path('authors/<str:authorId>/liked', LikedAPIs.as_view({"get": "getAuthorLiked"})),
    path('authors/<str:authorId>/posts/<str:postId>/liked/<str:likerId>', LikedAPIs.as_view({"get": "getAuthorPostLiked"})),

    #inbox
    path('authors/<str:authorId>/inbox', InboxAPIs.as_view({
        "get": "getInbox",
        "delete": "deleteInbox"
    })),
    path('inbox/public/<str:authorId>/<str:postId>', InboxAPIs.as_view({"post": "sendPublicPost"})),
    path('inbox/friend/<str:authorId>/<str:postId>', InboxAPIs.as_view({"post": "sendFriendPost"})),
    path('authors/<str:authorId>/inbox/<str:postId>', InboxAPIs.as_view({"post": "sendPost"})),

    #followRequests
    path('authors/<str:authorId>/followRequest', FollowRequestsAPIs.as_view({"get": "getFollowRequests"})),
    path('authors/<str:authorId>/followRequest/<str:foreignAuthorId>', FollowRequestsAPIs.as_view({
        "delete": "removeRequest",
        "get": "checkRequestedToFollow"})),
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

    #images
    path('images/<str:authorId>', ImagesAPIs.as_view({"put":"putImage", "get":"getImage"}))


]

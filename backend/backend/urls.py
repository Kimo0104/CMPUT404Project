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
from email.mime import base
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from database.views import PostsAPIs, CommentsAPIs, LikesAPIs, LikedAPIs, InboxAPIs

urlpatterns = [
    #admin
    path('admin/', admin.site.urls),

    #posts
    path('service/posts/<str:authorId>/posts/<str:postId>', PostsAPIs.as_view({"get": "getPost"})),
    path('service/posts/<str:authorId>/posts/<str:postId>', PostsAPIs.as_view({"post": "udpatePost"})),
    path('service/posts/<str:authorId>/posts/<str:postId>', PostsAPIs.as_view({"delete": "deletePost"})),
    path('service/posts/<str:authorId>/posts/<str:postId>', PostsAPIs.as_view({"put": "createPost"})),
    path('service/posts/<str:authorId>/posts/<str:postId>/image', PostsAPIs.as_view({"get": "getImagePost"})),

    #comments
    path('service/authors/<str:authorId>/posts/<str:postId>/comments', CommentsAPIs.as_view({"get": "getComments"})),
    path('service/authors/<str:authorId>/posts/<str:postId>/comments', CommentsAPIs.as_view({"get": "createComment"})),

    #likes
    path('service/authors/<str:authorId>/posts/<str:postId>/likes', LikesAPIs.as_view({"get": "getPostLikes"})),
    path('service/authors/<str:authorId>/posts/<str:postId>/comments/<str:commentId>/likes', LikesAPIs.as_view({"get": "getCommentLikes"})),

    #liked
    path('service/authors/<str:authorId>/likes', LikedAPIs.as_view({"get": "getAuthorLiked"})),

    #inbox
    path('service/authors/<str:authorId>/inbox', InboxAPIs.as_view({"get": "getInbox"})),
    path('service/authors/<str:authorId>/inbox', InboxAPIs.as_view({"post": "sendPost"})),
    path('service/authors/<str:authorId>/inbox', InboxAPIs.as_view({"post": "deleteInbox"})),

]

router = routers.SimpleRouter()
router.register(r'service/posts', PostsAPIs, basename = 'service/posts')
router.register(r'service/authors', CommentsAPIs, basename = 'service/authors')
router.register(r'service/authors', LikesAPIs, basename = 'service/authors')
router.register(r'service/authors', LikedAPIs, basename = 'service/authors')
router.register(r'service/authors', InboxAPIs, basename = 'service/authors')


urlpatterns = router.urls

from django.test import TestCase


from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Posts, Authors, Comments, Likes, LikesComments, Inbox, FollowRequests, Followers
from django.db.utils import IntegrityError
import json
import ast

class PostTest(APITestCase):
    def setUp(self):
        self.test_author = Authors.objects.create(
            id = 1,
            host = "test-host",
            displayName = "testAuthor", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
    def testGetPost(self):
        id = 1
        title = "This is a test"
        source = "test source"
        origin = "test origin"
        description = "test description"
        post_content = "test content"
        originalAuthor = self.test_author
        author = self.test_author
        self.test_post = Posts.objects.create(
            id = id,
            title = title,
            source = source,
            origin = origin,
            description = description,
            content = post_content,
            originalAuthor = originalAuthor,
            author = author
        )
        route = 'http://127.0.0.1:8000/authors/{}/posts'.format(self.test_author.id)
        response = self.client.get(route, format='json')
        content = ast.literal_eval(response.content.decode('utf-8'))
        assert(response.status_code == status.HTTP_200_OK)
        assert(content["count"] == 1)
        assert(content["posts"][0]["id"] == str(id))
        assert(content["posts"][0]["title"] == title)
        assert(content["posts"][0]["source"] == source)
        assert(content["posts"][0]["origin"] == origin)
        assert(content["posts"][0]["description"] == description)
        assert(content["posts"][0]["content"] == post_content)
        assert(content["posts"][0]["author"] == str(author.id))
        assert(content["posts"][0]["originalAuthor"] == str(originalAuthor.id))
    def testMakePost(self):
        data = {
            "type": "post",
            "title" : "This is a test",
            "source" : "test source",
            "origin" : "test origin",
            "description" : "test description",
            "contentType": "text/plain",
            "visibility": "PUBLIC",
            "content" : "test content",
            "originalAuthor" : 1,
            "author" : 1
        }
        route = 'http://127.0.0.1:8000/authors/{}/posts'.format(self.test_author.id)
        response = self.client.put(route, data, format='json')
        post = Posts.objects.get()
        assert(response.status_code == status.HTTP_200_OK)
        assert(post.type == data["type"])
        assert(post.title == data["title"])
        assert(post.source == data["source"])
        assert(post.origin == data["origin"])
        assert(post.description == data["description"])
        assert(post.contentType == data["contentType"])
        assert(post.visibility == data["visibility"])
        assert(post.content == data["content"])
        assert(post.originalAuthor.id == str(data["originalAuthor"]))
        assert(post.author.id == str(data["author"]))

    def testModifyPost(self):
        data = {
            "id": 1,
            "type": "post",
            "title" : "This is a test",
            "source" : "test source",
            "origin" : "test origin",
            "description" : "test description",
            "contentType": "text/plain",
            "visibility": "PUBLIC",
            "post_content" : "test content",
            "originalAuthor" : self.test_author,
            "author" : self.test_author
        }
        self.test_post = Posts.objects.create(
            id = data["id"],
            title = data["title"],
            source = data["source"],
            origin = data["origin"],
            description = data["description"],
            content = data["post_content"],
            originalAuthor = data["originalAuthor"],
            author = data["author"]
        )
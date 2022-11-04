from django.test import TestCase


from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Posts, Authors, Comments, Likes, LikesComments, Inbox, FollowRequests, Followers
from django.db.utils import IntegrityError
import json
import ast

class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user(
            username="testuser", 
            email="testuser@gmail.com",
            password="12345"
        )

    def test_user_exists(self):
        self.assertEqual(self.test_user.username,"testuser")
        self.assertEqual(self.test_user.email,"testuser@gmail.com")
    
    def test_create_user_with_preexisting_email(self):
        data = {
            "username": "testuser2",
            "email": "testuser2@gmail.com",
            "password": "testuser2"
        }

        response = self.client.put(reverse('authors'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email':  'testing',
            'passsword': 'foobarbaz'
        }

        response = self.client.put(reverse('authors'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_no_email(self):
        data = {
                'username' : 'foobar',
                'email': '',
                'password': 'foobarbaz'
        }

        response = self.client.put(reverse('authors'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

class CommentsAPITest(APITestCase):
    def setUp(self):
        self.test_author1 = Authors.objects.create(
            id = 1,
            host = "test-host",
            displayName = "testAuthor1",
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        ) 
        self.test_author2 = Authors.objects.create(
            id = 2,
            host = "test-host",
            displayName = "testAuthor2", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_post1 = Posts.objects.create(
            id = 1,
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author1,
            author = self.test_author1
        )
        self.test_post2 = Posts.objects.create(
            id = 2,
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author1,
            author = self.test_author1
        )
        self.test_comment1 = Comments.objects.create(
            id = 1,
            author = self.test_author2,
            post = self.test_post1,
            comment = "test comment"
        )
        self.test_comment2 = Comments.objects.create(
            id = 2,
            author = self.test_author2,
            post = self.test_post2,
            comment = "test comment"
        )

    # test getComment for post 1 returns only the comment for post 1
    def testGetCorrectComment(self):
        response = self.client.get(reverse('comments', args=[1,1]), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(len(response.data) == 1)
        assert(response.data[0]['id'] == "1")
        assert(response.data[0]['author'] == "2")
        assert(response.data[0]['post'] == "1")
        assert(response.data[0]['comment'] == "test comment")

    # test getComment for invalid post
    def testGetCommentWithInvalidPost(self):
        response = self.client.get(reverse('comments', args=[1,10]), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)

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
        response = self.client.get(reverse('post', args=[self.test_author.id]), format='json')
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
        response = self.client.put(reverse('post',args=[self.test_author.id]), data, format='json')
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
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Posts, Authors, Comments, Likes, LikesComments, Inbox, FollowRequests, Followers
from django.db.utils import IntegrityError
import ast

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
    def testGetPublicPost(self):
        id = 1
        title = "This is a test"
        source = "test source"
        origin = "test origin"
        description = "test description"
        post_content = "test content"
        originalAuthor = self.test_author
        author = self.test_author
        Posts.objects.create(
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
        Posts.objects.create(
            id = data["id"],
            title = data["title"],
            source = data["source"],
            origin = data["origin"],
            description = data["description"],
            content = data["post_content"],
            originalAuthor = data["originalAuthor"],
            author = data["author"]
        )
        modification = {
            "title" : "title after modification!"
        }
        response = self.client.post(reverse('existing-post',args=[self.test_author.id, data["id"]]), modification, format='json')
        assert(response.status_code == status.HTTP_200_OK)
        post = Posts.objects.get()
        assert(post.title == modification["title"])

    def testDeletePost(self):
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
        Posts.objects.create(
            id = data["id"],
            title = data["title"],
            source = data["source"],
            origin = data["origin"],
            description = data["description"],
            content = data["post_content"],
            originalAuthor = data["originalAuthor"],
            author = data["author"]
        )
        assert(len(Posts.objects.filter(id = data["id"])) == 1)
        response = self.client.delete(reverse('existing-post',args=[self.test_author.id, data["id"]]), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(len(Posts.objects.filter(id = data["id"])) == 0)

    def testGetPost(self):
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
        Posts.objects.create(
            id = data["id"],
            title = data["title"],
            source = data["source"],
            origin = data["origin"],
            description = data["description"],
            content = data["post_content"],
            originalAuthor = data["originalAuthor"],
            author = data["author"]
        )
        response = self.client.get(reverse('existing-post',args=[self.test_author.id, data["id"]]), format='json')
        content = ast.literal_eval(response.content.decode('utf-8'))
        assert(response.status_code == status.HTTP_200_OK)
        assert(content["id"] == str(data["id"]))
        assert(content["title"] == data["title"])
        assert(content["source"] == data["source"])
        assert(content["origin"] == data["origin"])
        assert(content["description"] == data["description"])
        assert(content["content"] == data["post_content"])
        assert(content["author"] == str(data["author"].id))
        assert(content["originalAuthor"] == str(data["originalAuthor"].id))

class FollowRequestsAPITest(APITestCase):
    def setUp(self):
        self.test_author = Authors.objects.create(
            id = 1,
            host = "test-host",
            displayName = "testAuthor", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_foreign_author = Authors.objects.create(
            id = 2,
            host = "test-host",
            displayName = "testForeignAuthor", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_follow_request = FollowRequests.objects.create(
            id = 1,
            receiver = self.test_foreign_author,
            requester = self.test_author
        )
    '''
    Ensures that getFollowRequests successfully returns the right follow request
    '''
    def testGetFollowRequests(self):
        response = self.client.get(reverse('get-follow-requests', args=[2]), format='json')
        assert(response.status_code==status.HTTP_200_OK)
        assert(len(response.data) == 1)
        assert(response.data[0]['id'] == "1")
        assert(response.data[0]['requester'] == "1")
        assert(response.data[0]['receiver'] == "2")
    '''
        Ensures that removeRequest successfully removes the follow request
    '''
    def testRemoveRequest(self):
        response = self.client.delete(reverse('manage-follow-requests', args=[2,1]), format='json')
        assert(response.status_code==status.HTTP_200_OK)
        assert(response.data['requester'] == "1")
        assert(response.data['receiver'] == "2")
    '''
        Ensures that checkRequestedToFollow successfully returns the object containing the follow request
    '''
    def testCheckRequestedToFollow(self):
        response = self.client.get(reverse('manage-follow-requests', args=[2,1]), format='json')
        assert(response.status_code==status.HTTP_200_OK)
        assert(response.data['requester'] == "1")
        assert(response.data['receiver'] == "2")

class FollowsAPITest(APITestCase):
    def setUp(self):
        self.test_author = Authors.objects.create(
            id = 1,
            host = "test-host",
            displayName = "testAuthor", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_foreign_author1 = Authors.objects.create(
            id = 2,
            host = "test-host",
            displayName = "testForeignAuthor1", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_foreign_author2= Authors.objects.create(
            id = 3,
            host = "test-host",
            displayName = "testForeignAuthor2", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_follow = Followers.objects.create(
            id = 1,
            follower = self.test_author,
            followed = self.test_foreign_author1
        )
        self.test_followRequest = FollowRequests.objects.create(
            id = 1,
            requester = self.test_foreign_author2,
            receiver = self.test_foreign_author1
        )
    '''
        Ensures that getFollowers successfully returns a list of the followers
    '''
    def testGetFollowers(self):
        response = self.client.get(reverse('get-followers', args=[2]), format='json')
        assert(response.status_code==status.HTTP_200_OK)
        assert(len(response.data) == 1)
        assert(response.data[0]['id'] == "1")
        assert(response.data[0]['follower'] == "1")
        assert(response.data[0]['followed'] == "2")
    '''
        Ensures that checkFollower successfully returns the object containing the follow relationship
    '''
    def testCheckFollower(self):
        response = self.client.get(reverse('manage-followers', args=[2,1]), format='json')
        assert(response.status_code==status.HTTP_200_OK)
        assert(response.data['id'] == "1")
        assert(response.data['follower'] == "1")
        assert(response.data['followed'] == "2")
    '''
        Ensures that addFollower successfully adds a follower
    '''
    def testAddFollower(self):
        response = self.client.put(reverse('manage-followers', args=[2,3]), format='json')
        assert(response.status_code==status.HTTP_200_OK)
    '''
        Ensures that removeFollower successfully adds a follower
    '''
    def testRemoveFollower(self):
        response = self.client.delete(reverse('manage-followers', args=[2,1]), format='json')
        assert(response.status_code==status.HTTP_200_OK)
    '''
        Ensures that requestToFollow successfully adds a follow request 
    '''
    def testRequestToFollow(self):
        response = self.client.post(reverse('manage-followers', args=[3,1]), format='json')
        assert(response.status_code==status.HTTP_200_OK)

class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", 
            email="testuser@gmail.com",
            password="12345"
        )
    
    # Test whether user gets created
    def test_create_user_with_preexisting_email(self):
        data = {
            "username": "testuser2",
            "email": "testuser2@gmail.com",
            "password": "testuser2"
        }
        response = self.client.post(reverse('users'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test user with empty credentials
    def test_create_user_with_no_info(self):
        data = {
                'username' : '',
                'email': '',
                'password': ''
        }

        response = self.client.put(reverse('authors'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
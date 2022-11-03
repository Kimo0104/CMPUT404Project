from django.test import TestCase


from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Posts, Authors
from django.db.utils import IntegrityError


class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL for creating an account.
        self.create_url = reverse('account-create')

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email':  'testing',
            'passsword': 'foobarbaz'
        }


        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
                'username' : 'foobar',
                'email': '',
                'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)


class PostsTests(TestCase):
    def setUp(self):
        self.test_author = Authors.objects.create(
            id = 1,
            host = "test-host",
            displayName = "testAuthor", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_post = Posts.objects.create(
            id = 1,
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author,
            author = self.test_author
        )
    '''
    Ensures that all default values are populated as expected
    '''
    def testDefaultValues(self):
        assert(self.test_post.type == "post")
        assert(self.test_post.contentType == 'text/plain')
        assert(self.test_post.count == 0)
        assert(self.test_post.visibility == "PUBLIC")
    '''
    Ensures that when an author is deleted. All their posts are deleted
    '''
    def testAuthorRemoval(self):
        posts = Posts.objects.filter(author = 1)
        assert(len(posts) > 0)
        self.test_author.delete()
        posts = Posts.objects.filter(author = 1)
        assert(len(posts) == 0)
    '''
    Ensures that when a post is created with an author that doesnt exist,
    an exception is raised.
    '''
    def testNonAuthoredPost(self):
        with self.assertRaisesRegexp(ValueError, '"Posts.author" must be a "Authors" instance.'):
            Posts.objects.create(
                id = 2,
                title = "This is a test",
                source = "test source",
                origin = "test origin",
                description = "test description",
                content = "test content",
                originalAuthor = self.test_author,
                author = 999
            )
    '''
    Ensures that when a post is created with an original author that doesnt exist,
    an exception is raised.
    '''
    def testNonOriginalAuthoredPost(self):
        with self.assertRaisesRegexp(ValueError, '"Posts.originalAuthor" must be a "Authors" instance.'):
            Posts.objects.create(
                id = 3,
                title = "This is a test",
                source = "test source",
                origin = "test origin",
                description = "test description",
                content = "test content",
                originalAuthor = 1,
                author = self.test_author
            )
    '''
    Ensures that when a post is made with an ID that already exists,
    an exception is raised.
    '''
    def testSamePostId(self):
        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            Posts.objects.create(
                id = 1,
                title = "This is a test",
                source = "test source",
                origin = "test origin",
                description = "test description",
                content = "test content",
                originalAuthor = self.test_author,
                author = self.test_author
            )
    '''
    Ensures that deleting the original author does not remove a post.
    '''
    def testDeletingOriginalAuthor(self):
        second_author = Authors.objects.create(
            id = 2,
            host = "test-host",
            displayName = "testAuthor2", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        Posts.objects.create(
                id = 4,
                title = "This is a test",
                source = "test source",
                origin = "test origin",
                description = "test description",
                content = "test content",
                originalAuthor = self.test_author,
                author = second_author
        )
        assert(len(Posts.objects.filter(id=4)) > 0)
        second_author.delete()
        assert(len(Posts.objects.filter(id=4)) == 0)
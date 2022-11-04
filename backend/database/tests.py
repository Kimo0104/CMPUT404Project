from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Posts, Authors, Comments, Likes, LikesComments, Inbox, FollowRequests, Followers
from django.db.utils import IntegrityError


class AccountsTest(TestCase):
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
        response = self.client.post('http://localhost:8000/users', data)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email':  'testing',
            'passsword': 'foobarbaz'
        }
        response = self.client.post("http://localhost:8000/users", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


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

class CommentsTest(TestCase):
    # create two authors
    # author 1 make a post
    # author 2 comments on post twice
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
        self.test_post = Posts.objects.create(
            id = 1,
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
            post = self.test_post,
            comment = "test comment"
        )
        self.test_comment2 = Comments.objects.create(
            id = 2,
            author = self.test_author2,
            post = self.test_post,
            comment = "test comment 2"
        )

    # test that default values are implemented correctly
    def testCommentDefaultValues(self):
        assert(self.test_comment1.type == 'comment')
        assert(self.test_comment1.contentType == 'text/plain')

    # test that two comments are created by an author for a given post
    # test that only two comments are made
    def testCommentCreation(self):
        assert(Comments.objects.filter(post=self.test_post).count() == 2)
        assert(Comments.objects.filter(author=self.test_author2).count() == 2)


    # test that another comment cannot be made with the same id
    def testCommentUniqueness(self):
        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            Comments.objects.create(
                id = 1,
                author = self.test_author2,
                post = self.test_post,
                comment = "test comment copy"
            )


    # test that a comment cannot be created with an invalid authorId
    def testCommentFromInvalidAuthor(self):
        with self.assertRaisesRegexp(ValueError, '"Comments.author" must be a "Authors" instance.'):
            Comments.objects.create(
                id = 3,
                author = 100,
                post = self.test_post,
                comment = "test comment copy"
            )

    # test that a comment cannot be created with an invalid postId
    def testCommentFromInvalidPost(self):
        with self.assertRaisesRegexp(ValueError, '"Comments.post" must be a "Posts" instance.'):
            Comments.objects.create(
                id = 3,
                author = self.test_author2,
                post = 10,
                comment = "test comment copy"
            )

    # test that a comment can be removed
    # test that only one comment is removed
    def testCommentDelete(self):
        self.test_comment1.delete()

        assert(Comments.objects.filter(id=1).count() == 0)
        assert(Comments.objects.all().count() == 1)

    # test that deleting the post deletes the comment
    def testDeleteParentPost(self):
        self.test_post.delete()
        self.test_post.save()

        assert(Comments.objects.all().count() == 0)

class LikesTest(TestCase):
    # mark initial counts of postLikes and commentLikes
    # create two authors
    # author 1 makes a post
    # author 2 comments on post
    # author 2 likes the post
    # author 1 likes the comment
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
        self.test_post = Posts.objects.create(
            id = 1,
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author1,
            author = self.test_author1
        )
        self.test_comment = Comments.objects.create(
            id = 1,
            author = self.test_author2,
            post = self.test_post,
            comment = "test comment"
        )
        self.test_post_like1 = Likes.objects.create(
            id = 1,
            context = self.test_post.title,
            summary = f'{self.test_author2.displayName} likes your post',
            author = self.test_author2,
            post = self.test_post
        )
        self.test_post_like2 = Likes.objects.create(
            id = 2,
            context = self.test_post.title,
            summary = f'{self.test_author2.displayName} likes your post',
            author = self.test_author2,
            post = self.test_post
        )
        self.test_comment_like1 = LikesComments.objects.create(
            id = 1,
            context = self.test_comment.comment,
            summary = f'{self.test_author2.displayName} likes your comment',
            author = self.test_author2,
            comment = self.test_comment
        )
        self.test_comment_like2 = LikesComments.objects.create(
            id = 2,
            context = self.test_comment.comment,
            summary = f'{self.test_author2.displayName} likes your comment',
            author = self.test_author2,
            comment = self.test_comment
        )

    # test that default values are implemented correctly
    def testLikesDefaultValues(self):
        assert(self.test_post_like1.type == 'like')
        assert(self.test_comment_like1.type == 'likescomment')

    # test that two likes of each kind are created by an author for a given post/comment
    # test that only two likes of each kind is made
    def testLikeCreation(self):
        assert(Likes.objects.filter(post=self.test_post).count() == 2)
        assert(Likes.objects.filter(author=self.test_author2).count() == 2)
        assert(LikesComments.objects.filter(comment=self.test_comment).count() == 2)
        assert(LikesComments.objects.filter(author=self.test_author2).count() == 2)
            
    # test that another post like cannot be made with the same id
    def testPostLikeUniqueness(self):
        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            Likes.objects.create(
                id = 1,
                context = self.test_post.title,
                summary = f'{self.test_author2.displayName} likes your post',
                author = self.test_author2,
                post = self.test_post
            )


    # test that another comment like cannot be made with the same id
    def testCommentLikeUniqueness(self):
        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            LikesComments.objects.create(
                id = 1,
                context = self.test_comment.comment,
                summary = f'{self.test_author2.displayName} likes your comment',
                author = self.test_author2,
                comment = self.test_comment
            )

    # test that a post like cannot be created with an invalid authorId
    def testPostLikeFromInvalidAuthor(self):
        with self.assertRaisesRegexp(ValueError, '"Likes.author" must be a "Authors" instance.'):
            Likes.objects.create(
                id = 3,
                context = self.test_post.title,
                summary = f'{self.test_author2.displayName} likes your post',
                author = 10,
                post = self.test_post
            )

    # test that a comment like cannot be created with an invalid authorId
    def testCommentLikeFromInvalidAuthor(self):
        with self.assertRaisesRegexp(ValueError, '"LikesComments.author" must be a "Authors" instance.'):
            LikesComments.objects.create(
                id = 3,
                context = self.test_comment.comment,
                summary = f'{self.test_author2.displayName} likes your comment',
                author = 10,
                comment = self.test_comment
            )

    # test that a post like cannot be created with an invalid postId
    def testPostLikeFromInvalidPost(self):
        with self.assertRaisesRegexp(ValueError, '"Likes.post" must be a "Posts" instance.'):
            Likes.objects.create(
                id = 3,
                context = self.test_post.title,
                summary = f'{self.test_author2.displayName} likes your post',
                author = self.test_author2,
                post = 10
            )

    # test that a comment like cannot be created with an invalid commentId
    def testCommentLikeFromInvalidComment(self):
        with self.assertRaisesRegexp(ValueError, '"LikesComments.comment" must be a "Comments" instance.'):
            LikesComments.objects.create(
                id = 3,
                context = self.test_comment.comment,
                summary = f'{self.test_author2.displayName} likes your comment',
                author = self.test_author2,
                comment = 10
            )

    # test that a post like can be removed
    # test that only one like is removed
    def testPostLikeDelete(self):
        self.test_post_like1.delete()
        assert(Likes.objects.filter(id=1).count() == 0)
        assert(Likes.objects.all().count() == 1)

    # test that a comment like can be removed
    # test that only one like is removed
    def testCommentLikeDelete(self):
        self.test_comment_like1.delete()
        assert(LikesComments.objects.filter(id=1).count() == 0)
        assert(LikesComments.objects.all().count() == 1)

    # test that deleting the post deletes the like
    def testDeleteParentPost(self):
        self.test_post.delete()
        assert(Likes.objects.all().count() == 0)

    # test that deleting the post deletes the like
    def testDeleteParentComment(self):
        self.test_comment.delete()
        assert(LikesComments.objects.all().count() == 0)


class InboxTests(TestCase):
    def setUp(self):
        # make two authors
        # author 1 makes a post
        # add post to inbox of author 2
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
        self.test_post = Posts.objects.create(
            id = 1,
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author1,
            author = self.test_author1
        )
        self.test_inbox = Inbox.objects.create(
            id = 1,
            author = self.test_author2,
            post = self.test_post
        )

    # test that one inbox entry was made for that post and for that author
    # test that only one inbox entry was made
    def testInboxCreation(self):
        assert(Inbox.objects.filter(post=self.test_post).count() == 1)
        assert(Inbox.objects.filter(author=self.test_author2).count() == 1)
        assert(Inbox.objects.all().count() == 1)


    # test that another inbox entry cannot be made with the same id
    def testInboxUniqueness(self):
        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            Inbox.objects.create(
                id = 1,
                author = self.test_author2,
                post = self.test_post
            )


    # test that an inbox entry cannot be created with an invalid authorId
    def testInboxFromInvalidAuthor(self):
        with self.assertRaisesRegexp(ValueError, '"Inbox.author" must be a "Authors" instance.'):
            Inbox.objects.create(
                id = 2,
                author = 10,
                post = self.test_post
            )

    # test that an inbox entry cannot be created with an invalid postId
    def testInboxWithInvalidPost(self):
        with self.assertRaisesRegexp(ValueError, '"Inbox.post" must be a "Posts" instance.'):
            Inbox.objects.create(
                id = 2,
                author = self.test_author2,
                post = 10
            )

    # test that an inbox entry can be removed
    # test that only one inbox entry is removed
    def testInboxDelete(self):
        self.sample_test_inbox = Inbox.objects.create(
            id = 2,
            author = self.test_author2,
            post = self.test_post
        )
        self.sample_test_inbox.save()
        self.test_inbox.delete()

        assert(Inbox.objects.filter(id=1).count() == 0)
        assert(Inbox.objects.all().count() == 1)

    # test that deleting the author deletes the inbox
    def testDeleteParentAuthor(self):
        self.test_post.delete()
        assert(Inbox.objects.all().count() == 0)

    # test that deleting the post deletes the inbox
    def testDeleteParentPost(self):
        self.test_post.delete()
        assert(Inbox.objects.all().count() == 0)
            
class FollowRequestsTests(TestCase):
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
    Ensures that the default values are populated as expected
    '''
    def testDefaultRelationship(self):
        authorRequests = FollowRequests.objects.filter(requester = 1)
        assert(len(authorRequests) == 1)
        foreignAuthorRequests = FollowRequests.objects.filter(receiver = 2)
        assert(len(foreignAuthorRequests) == 1)
    '''
    Ensures that when an author is deleted, their follow requests would no longer exist
    '''
    def testAuthorRemoval(self):
        authorRequests = FollowRequests.objects.filter(requester = 1)
        assert(len(authorRequests) == 1)
        self.test_author.delete()
        authorRequests = FollowRequests.objects.filter(requester = 1)
        assert(len(authorRequests) == 0)
    '''
    Ensures that when a foreign author is deleted, their follow requests would no longer exist
    '''
    def testForeignAuthorRemoval(self):
        foreignAuthorRequests = FollowRequests.objects.filter(receiver = 2)
        assert(len(foreignAuthorRequests) == 1)
        self.test_foreign_author.delete()
        foreignAuthorRequests = FollowRequests.objects.filter(receiver = 2)
        assert(len(foreignAuthorRequests) == 0)
    '''
    Ensures that when a follow request is created with an author/foreign author that doesnt exist,
    an exception is raised.
    '''
    def testNonAuthoredFollowRequests(self):
        with self.assertRaisesRegexp(ValueError, '"FollowRequests.requester" must be a "Authors" instance.'):
            FollowRequests.objects.create(
                id = 2,
                requester = 999,
                receiver = self.test_foreign_author
            )
        with self.assertRaisesRegexp(ValueError, '"FollowRequests.receiver" must be a "Authors" instance.'):
            FollowRequests.objects.create(
                id = 2,
                requester = self.test_author,
                receiver = 999
            )
    '''
    Ensures that when a follow request is made with an ID that already exists,
    an exception is raised.
    '''
    def testSamePostId(self):
        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            FollowRequests.objects.create(
                id = 1,
                requester = self.test_author,
                receiver = self.test_foreign_author
            )

class FollowsTests(TestCase):
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
        self.test_follow = Followers.objects.create(
            id = 1,
            follower = self.test_author,
            followed = self.test_foreign_author
        )
    '''
    Ensures that the default values are populated as expected
    '''
    def testDefaultRelationship(self):
        authorRelationship = Followers.objects.filter(follower = 1)
        assert(len(authorRelationship) == 1)
        foreignAuthorRelationship = Followers.objects.filter(followed = 2)
        assert(len(foreignAuthorRelationship) == 1)
    '''
    Ensures that when an author is deleted, their follow relationship would no longer exist
    '''
    def testAuthorRemoval(self):
        authorRelationship = Followers.objects.filter(follower = 1)
        assert(len(authorRelationship) == 1)
        self.test_author.delete()
        authorRelationship = Followers.objects.filter(follower = 1)
        assert(len(authorRelationship) == 0)
    '''
    Ensures that when a foreign author is deleted, their follow relationship would no longer exist
    '''
    def testAuthorRemoval(self):
        foreignAuthorRelationship = Followers.objects.filter(follower = 1)
        assert(len(foreignAuthorRelationship) == 1)
        self.test_foreign_author.delete()
        foreignAuthorRelationship = Followers.objects.filter(follower = 1)
        assert(len(foreignAuthorRelationship) == 0)
    '''
    Ensures that when a follow relationship is created with an author/foreign author that doesnt exist,
    an exception is raised.
    '''
    def testNonAuthoredFollowRequests(self):
        with self.assertRaisesRegexp(ValueError, 'Followers.follower" must be a "Authors" instance.'):
            Followers.objects.create(
                id = 2,
                follower = 999,
                followed = self.test_foreign_author
            )
        with self.assertRaisesRegexp(ValueError, 'Followers.followed" must be a "Authors" instance.'):
            Followers.objects.create(
                id = 2,
                follower = self.test_author,
                followed = 999
            )
    '''
    Ensures that when a follow relationship is made with an ID that already exists,
    an exception is raised.
    '''
    def testSamePostId(self):
        with self.assertRaisesRegexp(IntegrityError, "duplicate key value violates unique constraint"):
            Followers.objects.create(
                id = 1,
                follower = self.test_author,
                followed = self.test_foreign_author
            )
    


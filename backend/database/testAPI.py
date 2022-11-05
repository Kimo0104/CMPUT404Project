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

class CommentsTest(APITestCase):
    def setUp(self):
        self.test_author1 = Authors.objects.create(
            id = "1",
            host = "test-host",
            displayName = "testAuthor1",
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        ) 
        self.test_author2 = Authors.objects.create(
            id = "2",
            host = "test-host",
            displayName = "testAuthor2", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_post1 = Posts.objects.create(
            id = "1",
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author1,
            author = self.test_author1
        )
        self.test_comment1 = Comments.objects.create(
            id = "1",
            author = self.test_author2,
            post = self.test_post1,
            comment = "test comment"
        )

    # test getComment for post 1 returns only the comments for post 1
    def testGetCorrectComment(self):
        response = self.client.get(reverse('comments', args=[self.test_author1.id,self.test_post1.id]), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(len(response.data) == 1)
        assert(response.data[0]['id'] == "1")
        assert(response.data[0]['author'] == "2")
        assert(response.data[0]['post'] == "1")
        assert(response.data[0]['comment'] == "test comment")

    # test getComment for invalid post
    def testGetCommentWithInvalidPost(self):
        response = self.client.get(reverse('comments', args=[self.test_author1.id,10]), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)

    # test createComment for creating exactly one comment as specified
    def testCreateCorrectComment(self):
        commentStr = 'this is a test comment!'
        data = {
            'comment' : commentStr
        }
        response = self.client.post(reverse('comments', args=[self.test_author2.id,self.test_post1.id]), data, format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(Comments.objects.all().count() == 2) # one extra

        createdComment = Comments.objects.get(comment=commentStr)
        assert(createdComment.comment == commentStr)
        assert(createdComment.contentType == 'text/plain')
        assert(createdComment.author.id == self.test_author2.id)
        assert(createdComment.post.id == self.test_post1.id)

    # test createComment for invalid author
    def testCreateCommentWithInvalidAuthor(self):
        data = {
            'comment' : 'this is a test comment!'
        }
        response = self.client.post(reverse('comments', args=["10",self.test_post1.id]), data, format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Comments.objects.all().count() == 1) # no extra comments

    # test createComment for invalid post
    def testCreateCommentWithInvalidPost(self):
        data = {
            'comment' : 'this is a test comment!'
        }
        response = self.client.post(reverse('comments', args=[self.test_author2.id,10]), data, format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Comments.objects.all().count() == 1) # no extra comments

    # test createComment for invalid contentType
    def testCreateCommentWithInvalidContentType(self):
        data = {
            'comment' : 'this is a test comment!',
            'contentType': 'invalid'
        }
        response = self.client.post(reverse('comments', args=[self.test_author2.id,self.test_post1.id]), data, format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Comments.objects.all().count() == 1) # no extra comments

    # test createComment with invalid content
    def testCreateCommentWithInvalidContent(self):
        data = {
            'comment' : ''
        }
        response = self.client.post(reverse('comments', args=[self.test_author2.id,self.test_post1.id]), data, format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Comments.objects.all().count() == 1) # no extra comments


class LikesTest(APITestCase):
    def setUp(self):
        #create three authors
        #author 1 makes a post
        #author 2 makes a comment
        #other authors like the post
        #other authors like the comment
        self.test_author1 = Authors.objects.create(
            id = "1",
            host = "test-host",
            displayName = "testAuthor1",
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        ) 
        self.test_author2 = Authors.objects.create(
            id = "2",
            host = "test-host",
            displayName = "testAuthor2", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_author3 = Authors.objects.create(
            id = "3",
            host = "test-host",
            displayName = "testAuthor3",
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        ) 
        self.test_post = Posts.objects.create(
            id = "1",
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author1,
            author = self.test_author1
        )
        self.test_comment = Comments.objects.create(
            id = "1",
            author = self.test_author2,
            post = self.test_post,
            comment = "test comment"
        )
        self.test_post_like1 = Likes.objects.create(
            id = "1",
            context = self.test_post.title,
            summary = f'{self.test_author2.displayName} likes your post',
            author = self.test_author2,
            post = self.test_post
        )
        self.test_comment_like1 = LikesComments.objects.create(
            id = "1",
            context = self.test_comment.comment,
            summary = f'{self.test_author1.displayName} likes your comment',
            author = self.test_author1,
            comment = self.test_comment
        )

    '''
    test createPostLike by creating one post like for post 1
    '''
    def testCreateCorrectPostLike(self):
        args = [self.test_author1.id,self.test_post.id,self.test_author3.id]
        response = self.client.post(reverse('post-like', args=args), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(Likes.objects.all().count() == 2) # one extra

        createdPostLike = Likes.objects.get(author=self.test_author3)
        assert(createdPostLike.context == self.test_post.title)
        assert(createdPostLike.summary == f'{self.test_author3.displayName} likes your post')
        assert(createdPostLike.author.id == self.test_author3.id)
        assert(createdPostLike.post.id == self.test_post.id)

    '''
    test createPostlike with invalid postId
    '''
    def testCreatePostLikeWithInvalidPost(self):
        args = [self.test_author1.id,10,self.test_author3.id]
        response = self.client.post(reverse('post-like', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test createPostlike with invalid likerId
    '''
    def testCreatePostLikeWithInvalidLiker(self):
        args = [self.test_author1.id,self.test_post.id,10]
        response = self.client.post(reverse('post-like', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test createPostlike by trying to like the same post twice
    '''
    def testCreatePostLikeWithInvalidLiker(self):
        args = [self.test_author1.id,self.test_post.id,self.test_author2.id]
        response = self.client.post(reverse('post-like', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test createCommentLike by creating one comment like for comment 1
    '''
    def testCreateCorrectCommentLike(self):
        args = [self.test_author1.id,self.test_post.id,self.test_comment.id,self.test_author3.id]
        response = self.client.post(reverse('comment-like', args=args), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(LikesComments.objects.all().count() == 2) # one extra

        createdCommentLike = LikesComments.objects.get(author=self.test_author3)
        assert(createdCommentLike.context == self.test_comment.comment)
        assert(createdCommentLike.summary == f'{self.test_author3.displayName} likes your comment')
        assert(createdCommentLike.author.id == self.test_author3.id)
        assert(createdCommentLike.comment.id == self.test_comment.id)

    '''
    test createCommentlike with invalid commentId
    '''
    def testCreateCommentLikeWithInvalidPost(self):
        args = [self.test_author1.id,self.test_post.id,10,self.test_author3.id]
        response = self.client.post(reverse('comment-like', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(LikesComments.objects.all().count() == 1)

    '''
    test createCommentlike with invalid likerId
    '''
    def testCreateCommentLikeWithInvalidLiker(self):
        args = [self.test_author1.id,self.test_post.id,self.test_comment.id,10]
        response = self.client.post(reverse('comment-like', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(LikesComments.objects.all().count() == 1)

    '''
    test createCommentlike by trying to like the same comment twice
    '''
    def testCreateCommentLikeWithInvalidLiker(self):
        args = [self.test_author1.id,self.test_post.id,self.test_comment.id,self.test_author1.id]
        response = self.client.post(reverse('comment-like', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(LikesComments.objects.all().count() == 1)

    '''
    test deletePostLike by trying to delete an existing like properly
    '''
    def testDeletePostLike(self):
        args = [self.test_author1.id,self.test_post.id,self.test_author2.id]
        response = self.client.delete(reverse('post-like', args=args))
        assert(response.status_code == status.HTTP_200_OK)
        assert(Likes.objects.all().count() == 0)

    '''
    test deletePostLike by trying to delete a non-existing like
    '''
    def testDeleteInvalidPostLike(self):
        args = [self.test_author1.id,self.test_post.id,self.test_author3.id]
        response = self.client.delete(reverse('post-like', args=args))
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test deletePostLike by trying to delete a like from a non-existing post
    '''
    def testDeletePostLikeInvalidPost(self):
        args = [self.test_author1.id,10,self.test_author2.id]
        response = self.client.delete(reverse('post-like', args=args))
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test deletePostLike by trying to delete a like from a non-existing liker
    '''
    def testDeletePostLikeInvalidLiker(self):
        args = [self.test_author1.id,self.test_post.id,10]
        response = self.client.delete(reverse('post-like', args=args))
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test deleteCommentLike by trying to delete an existing like properly
    '''
    def testDeleteCommentLike(self):
        args = [self.test_author1.id,self.test_post.id,self.test_comment.id,self.test_author1.id]
        response = self.client.delete(reverse('comment-like', args=args))
        assert(response.status_code == status.HTTP_200_OK)
        assert(LikesComments.objects.all().count() == 0)

    '''
    test deleteCommentLike by trying to delete a non-existing like
    '''
    def testDeleteInvalidCommentLike(self):
        args = [self.test_author1.id,self.test_post.id,self.test_comment.id,self.test_author3.id]
        response = self.client.delete(reverse('comment-like', args=args))
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test deleteCommentLike by trying to delete a non-existing comment
    '''
    def testDeleteCommentLikeInvalidComment(self):
        args = [self.test_author1.id,self.test_post.id,10,self.test_author1.id]
        response = self.client.delete(reverse('comment-like', args=args))
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test deleteCommentLike by trying to delete a like from a non-existing liker
    '''
    def testDeleteCommentLikeInvalidLiker(self):
        args = [self.test_author1.id,self.test_post.id,self.test_comment.id,10]
        response = self.client.delete(reverse('comment-like', args=args))
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
        assert(Likes.objects.all().count() == 1)

    '''
    test getPostLikes by getting all post likes
    '''
    def testGetPostLikes(self):
        args = [self.test_author1.id,self.test_post.id]
        response = self.client.get(reverse('get-post-like', args=args), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(len(response.data) == 1)
    
    '''
    test getPostLikes pagination
    '''
    def testGetPostLikesPagination(self):
        test_author4 = Authors.objects.create(
            id = "4",
            host = "test-host",
            displayName = "testAuthor4", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        Likes.objects.create(
            id = "2",
            context = self.test_post.title,
            summary = f'{self.test_author3.displayName} likes your post',
            author = self.test_author3,
            post = self.test_post
        )
        Likes.objects.create(
            id = "3",
            context = self.test_post.title,
            summary = f'{test_author4.displayName} likes your post',
            author = test_author4,
            post = self.test_post
        )
        args = [self.test_author1.id,self.test_post.id]
        response = self.client.get(reverse('get-post-like', args=args), {'page': 1,'size': 3}, format='json')
        assert(len(response.data) == 3)
        response = self.client.get(reverse('get-post-like', args=args), {'page': 2,'size': 2}, format='json')
        assert(len(response.data) == 1)
        response = self.client.get(reverse('get-post-like', args=args), {'page': 3,'size': 5}, format='json')
        assert(len(response.data) == 0)

    
    '''
    test getPostLikes with an invalid postId
    '''
    def testGetPostLikesWithInvalidPostId(self):
        args = [self.test_author1.id,10]
        response = self.client.get(reverse('get-post-like', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)

    '''
    test getCommentLikes by getting all comment likes
    '''
    def testGetCommentLikes(self):
        args = [self.test_author1.id,self.test_post.id,self.test_comment.id]
        response = self.client.get(reverse('get-comment-like', args=args), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(len(response.data) == 1)
    
    '''
    test getCommentLikes pagination
    '''
    def testCommentLikesPagination(self):
        test_author4 = Authors.objects.create(
            id = "4",
            host = "test-host",
            displayName = "testAuthor4", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )        
        self.test_comment_like2 = LikesComments.objects.create(
            id = "2",
            context = self.test_comment.comment,
            summary = f'{self.test_author3.displayName} likes your comment',
            author = self.test_author3,
            comment = self.test_comment
        )
        self.test_comment_like3 = LikesComments.objects.create(
            id = "3",
            context = self.test_comment.comment,
            summary = f'{test_author4.displayName} likes your comment',
            author = test_author4,
            comment = self.test_comment
        )
        args = [self.test_author2.id,self.test_post.id,self.test_comment.id]
        response = self.client.get(reverse('get-comment-like', args=args), {'page': 1,'size': 3}, format='json')
        assert(len(response.data) == 3)
        response = self.client.get(reverse('get-comment-like', args=args), {'page': 2,'size': 2}, format='json')
        assert(len(response.data) == 1)
        response = self.client.get(reverse('get-comment-like', args=args), {'page': 3,'size': 5}, format='json')
        assert(len(response.data) == 0)
    
    '''
    test getCommentLikes with an invalid commentId
    '''
    def testGetCommentLikes(self):
        args = [self.test_author1.id,self.test_post.id,10]
        response = self.client.get(reverse('get-comment-like', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)


class LikedTests(APITestCase):
    def setUp(self):
        # make two authors
        # author 1 makes a post
        # author 1 makes a comment
        # author 2 likes the post
        # author 2 likes the comment
        self.test_author1 = Authors.objects.create(
            id = "1",
            host = "test-host",
            displayName = "testAuthor1",
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        ) 
        self.test_author2 = Authors.objects.create(
            id = "2",
            host = "test-host",
            displayName = "testAuthor2", 
            url = "test-url",
            github = "github.com",
            profileImage = "image"
        )
        self.test_post = Posts.objects.create(
            id = "1",
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author1,
            author = self.test_author1
        )
        self.test_comment = Comments.objects.create(
            id = "1",
            author = self.test_author1,
            post = self.test_post,
            comment = "test comment"
        )
        self.test_post_like1 = Likes.objects.create(
            id = "1",
            context = self.test_post.title,
            summary = f'{self.test_author2.displayName} likes your post',
            author = self.test_author2,
            post = self.test_post
        )
        self.test_comment_like1 = LikesComments.objects.create(
            id = "1",
            context = self.test_comment.comment,
            summary = f'{self.test_author2.displayName} likes your comment',
            author = self.test_author2,
            comment = self.test_comment
        )

    '''
    test getAuthorPostLiked returns true on a post the author has liked
    '''
    def testGetAuthorPostsLikedTrue(self):
        args = [self.test_author1.id, self.test_post.id, self.test_author2.id]
        response = self.client.get(reverse('has-liked', args=args), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(response.data)

    '''
    test getAuthorPostLiked returns false on a post the author has not liked
    '''
    def testGetAuthorPostsLikedFalse(self):
        args = [self.test_author1.id, self.test_post.id, self.test_author1.id]
        response = self.client.get(reverse('has-liked', args=args), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(not response.data)

    '''
    test getAuthorPostLiked with an invalid postId
    '''
    def testGetAuthorPostsLikedWithInvalidPost(self):
        args = [self.test_author1.id, 10, self.test_author2.id]
        response = self.client.get(reverse('has-liked', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)

    '''
    test getAuthorPostLiked with an invalid likerId
    '''
    def testGetAuthorPostsLikedWithInvalidLiker(self):
        args = [self.test_author1.id, self.test_post.id, 10]
        response = self.client.get(reverse('has-liked', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
    
    '''
    test getAuthorLiked by getting all things liked
    '''
    def testGetAuthorLiked(self):
        args = [self.test_author2.id]
        response = self.client.get(reverse('liked', args=args), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(len(response.data) == 2)
    
    '''
    test getAuthorLiked pagination
    '''
    def testGetPostLikesPagination(self):
        test_post2 = Posts.objects.create(
            id = "2",
            title = "This is a test",
            source = "test source",
            origin = "test origin",
            description = "test description",
            content = "test content",
            originalAuthor = self.test_author1,
            author = self.test_author1
        )
        test_comment2 = Comments.objects.create(
            id = "2",
            author = self.test_author1,
            post = self.test_post,
            comment = "test comment"
        )
        Likes.objects.create(
            id = "2",
            context = test_post2.title,
            summary = f'{self.test_author2.displayName} likes your post',
            author = self.test_author2,
            post = test_post2
        )
        LikesComments.objects.create(
            id = "2",
            context = test_comment2.comment,
            summary = f'{self.test_author2.displayName} likes your comment',
            author = self.test_author2,
            comment = test_comment2
        )
        args = [self.test_author2.id]
        response = self.client.get(reverse('liked', args=args), {'page': 1,'size': 3}, format='json')
        assert(len(response.data) == 3)
        response = self.client.get(reverse('liked', args=args), {'page': 2,'size': 3}, format='json')
        assert(len(response.data) == 1)
        response = self.client.get(reverse('liked', args=args), {'page': 3,'size': 5}, format='json')
        assert(len(response.data) == 0)

    
    '''
    test getAuthorLiked with an invalid authorId
    '''
    def testGetAuthorLikedWithInvalidAuthorId(self):
        args = [10]
        response = self.client.get(reverse('liked', args=args), format='json')
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)


class InboxTest(APITestCase):
    def setUp(self):
        pass

    


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
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
        # make two authors
        # author 1 makes a post
        # author 1 makes a comment on post
        # author 2 make a comment on post
        # author 2 likes post
        # author 2 likes author 1s comment
        # post 1 goes into author 1s inbox
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
        self.test_comment1 = Comments.objects.create(
            id = "1",
            author = self.test_author1,
            post = self.test_post,
            comment = "test comment"
        )
        self.test_comment2 = Comments.objects.create(
            id = "2",
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
            context = self.test_comment1.comment,
            summary = f'{self.test_author2.displayName} likes your comment',
            author = self.test_author2,
            comment = self.test_comment1
        )
        self.inbox = Inbox.objects.create(
            id = "1",
            author = self.test_author1,
            post = self.test_post
        )

    '''
    test getInbox by getting all things in inbox
    '''
    def testGetInbox(self):
        args = [self.test_author1.id]
        response = self.client.get(reverse('inbox', args=args), format='json')
        assert(response.status_code == status.HTTP_200_OK)
        assert(len(response.data["inbox"]) == 5) #the post, like, comments, comment like
        assert(response.data["count"] == 5)
    
    '''
    test getInbox pagination
    '''
    def testGetInboxPagination(self):
        args = [self.test_author1.id]
        response = self.client.get(reverse('inbox', args=args), {'page': 1,'size': 3}, format='json')
        assert(len(response.data["inbox"]) == 3)
        response = self.client.get(reverse('inbox', args=args), {'page': 2,'size': 3}, format='json')
        assert(len(response.data["inbox"]) == 2)
        response = self.client.get(reverse('inbox', args=args), {'page': 3,'size': 5}, format='json')
        assert(len(response.data["inbox"]) == 0)

    
    '''
    test getInbox with an invalid authorId
    '''
    def testGetInboxWithInvalidAuthorId(self):
        args = [10]
        response = self.client.get(reverse('inbox', args=args), format='json')
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
    
class AuthorsTest(APITestCase):
    def setUp(self):
        # Creates Authors with IDs 1 to 10 (We need multiple authors to test
        # pagination in some API methods)
        self.test_author = Authors.objects.create(
                            id="1", 
                            host="//service", 
                            displayName="test_author_1", 
                            url="//service/author/1", 
                            github="http://github.com/test_author_1", 
                            accepted=True, 
                            profileImage="url_to_profile_image"
                            )
        User.objects.create(username=self.test_author.displayName, email="test_", password="test")
        for i in range(2, 11):
            test_author_i = Authors.objects.create(
                                id=str(i), 
                                host="//service", 
                                displayName=f"test_author_{i}", 
                                url=f"//service/author/{i}", 
                                github=f"http://github.com/test_author_{i}", 
                                accepted=True, 
                                profileImage="url_to_profile_image"
                                )
            User.objects.create(username=test_author_i.displayName, email=f"test_{i}", password="test")
        

    '''
    Tests the getAuthor API method when getting an author that already exists.
    '''
    def testGetExistingAuthor(self):
        response = self.client.get(reverse('manage-authors', args=[str(self.test_author.id)]), format="json")
        assert(response.status_code == status.HTTP_200_OK)
        assert(len(response.data) == len(Authors._meta.fields))
        returned_author = response.data
        assert(returned_author["id"] == str(self.test_author.id))
        assert(returned_author["type"] == self.test_author.type)
        assert(returned_author["host"] == self.test_author.host)
        assert(returned_author["displayName"] == self.test_author.displayName)
        assert(returned_author["url"] == self.test_author.url)
        assert(returned_author["github"] == self.test_author.github)
        assert(returned_author["accepted"] == self.test_author.accepted)
        assert(returned_author["profileImage"] == self.test_author.profileImage)
    
    '''
    Tests the getAuthor API method when getting an Authors that does not exist.
    '''
    def testGetNonExistingAuthor(self):
        response = self.client.get(reverse('manage-authors', args=["100"]), format="json")
        assert(response.status_code == status.HTTP_404_NOT_FOUND)
    
    '''
    Tests that editing an existing author actually modifies that Authors object in the
    database.
    '''
    def testPostToExistingAuthorWithValidData(self):
        # The only fields that are editable are github and profileImage.
        data = {
            "github": "http://github.com/new_github_url",
            "profileImage": "new_profileImage_url"
        }
        response = self.client.post(reverse('manage-authors', args=["1"]), data, format="json")
        assert(response.status_code == status.HTTP_202_ACCEPTED)
        # self.test_author contains outdated data now, so we get the updatedAuthor
        # by getting the Authors object with the same id
        updatedAuthor = Authors.objects.get(id=self.test_author.id)
        assert(updatedAuthor.github == data["github"])
        assert(updatedAuthor.profileImage == data["profileImage"])
    
    '''
    Tests that trying to edit an author that does not exist returns the proper
    response (404 NOT FOUND)
    '''
    def testPostToNonExistingAuthor(self):
        data = {
            "github": "http://github.com/new_github_url",
            "profileImage": "new_profileImage_url"
        }
        response = self.client.post(reverse('manage-authors', args=["100"]), data, format="json")
        assert(response.status_code == status.HTTP_404_NOT_FOUND)
    
    '''
    Tests that sending a POST request with a body containing data in a format
    other than JSON returns 400 BAD REQUEST
    '''
    def testPostToExistingAuthorWithNonJSONBody(self):
        data = "profileImage=new_profileImage_url"
        response = self.client.post(reverse('manage-authors', args=["1"]), data, format="json")
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
    
    '''
    Tests that sending a request that tries to edit fields that are not editable or 
    don't exist returns 400 BAD REQUEST
    '''
    def testPostToExistingAuthorWithInvalidFields(self):
        data = {
            "displayName": "new_display_name"
        }
        response = self.client.post(reverse('manage-authors', args=["1"]), data, format="json")
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
    
    '''
    Tests that the getAuthors API method works as expected, i.e. returns the appropriate
    page with the appropriate page_size.
    '''
    def testGetMultipleAuthors(self):
        data = {
            "page": 2,
            "size": 3
        }
        response = self.client.get(reverse('authors'), data, format="json")
        assert(len(response.data) == 2)
        assert(len(response.data["authorsPage"]) == 3)
        assert(response.data["numPages"] == "4")  # There are 4 pages total, 4 = ceil(10/3)

        # Now make sure that the 4th page only has 1 item
        data["page"] = 4
        response = self.client.get(reverse('authors'), data, format="json")
        assert(len(response.data["authorsPage"]) == 1)


    '''
    Tests that the findAuthors API method works as expected. I will be searching for 
    authors whose displayNames contain "1", there should be two authors.
    '''
    def testFindAuthors(self):
        # Making sure pagination works right in this method as well,
        # there should exist an author on both page 1 and page 2 with 
        # this query.
        page_1_query = {
            "query": "1",
            "page": "1",
            "size": "1"
        }
        page_2_query = {
            "query": "1",
            "page": "2",
            "size": "1"
        }
        response_1 = self.client.get(reverse('find-authors'), page_1_query, format="json")
        response_2 = self.client.get(reverse('find-authors'), page_2_query, format="json")
        assert(len(response_1.data) == len(response_2.data) and len(response_1.data) == 2)
        assert(response_1.data["numPages"] == response_2.data["numPages"])
        assert(len(response_1.data["authorsPage"]) == 1 and len(response_1.data["authorsPage"]) == 1)
        assert("1" in response_1.data["authorsPage"][0]["displayName"])
        assert("1" in response_2.data["authorsPage"][0]["displayName"])

    '''
    Tests that the createAuthor API method works as expected, with valid input. 
    '''    
    def testCreateNewAuthor(self):
        data = {
            "authorId": "11",
            "displayName": "test_creation"
        }
        response = self.client.put(reverse('authors'), data, format="json")
        assert(response.status_code == status.HTTP_201_CREATED)
        created_author = Authors.objects.filter(id=data["authorId"])
        assert(created_author.count() == 1)
        created_author = Authors.objects.get(id=data["authorId"])
        assert(created_author.id == data["authorId"])
        assert(created_author.displayName == data["displayName"])
    
    '''
    Tests that the createAuthor API method returns a 400 Bad Request if given a PUT request body
    containing data in a format other than JSON
    '''
    def testCreateNewAuthorNonJSONData(self):
        data = "authorId=11&displayName=test_creation"
        response = self.client.put(reverse('authors'), data, format="json")
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
    
    '''
    Tests that the createAuthor API method returns a 400 Bad Request if it is given a
    body in JSON format but missing the "authorId" key
    '''
    def testCreateNewAuthorNoAuthorId(self):
        data = {
            "displayName": "test_author_creation"
        }
        response = self.client.put(reverse('authors'), data, format="json")
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)

    '''
    Tests that the createAuthor API method returns a 400 Bad Request if it is given a
    body in JSON format but missing the "displayName" key
    '''
    def testCreateNewAuthorNoDisplayName(self):
        data = {
            "authorId": "11"
        }
        response = self.client.put(reverse('authors'), data, format="json")
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)
    
    '''
    Tests that the createAuthor API method returns a 409 Conflict if the authorId that 
    is passed to it already exists in the database
    '''
    def testCreateNewAuthorDuplicateAuthorId(self):
        data = {
            "authorId": "1",
            "displayName": "test_author_creation"
        }
        response = self.client.put(reverse('authors'), data, format="json")
        assert(response.status_code == status.HTTP_409_CONFLICT)

    '''
    Tests that the createAuthor API method returns a 409 Conflict if the displayName that 
    is passed to it already exists in the database
    '''
    def testCreateNewAuthorDuplicateAuthorId(self):
        data = {
            "authorId": "11",
            "displayName": "test_author_1"
        }
        response = self.client.put(reverse('authors'), data, format="json")
        assert(response.status_code == status.HTTP_409_CONFLICT)

    

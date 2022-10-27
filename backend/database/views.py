import io
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import io
from collections import defaultdict
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator
#Models defines how their objects are stored in the database
#serializers defines how to convert a post object to JSON
from .models import Authors, Posts, Comments, Likes, LikesComments, Inbox, Followers, FollowRequests
from .serializers import AuthorSerializer, PostsSerializer, CommentsSerializer, LikesSerializer, LikesCommentsSerializer, InboxSerializer, FollowersSerializer, FollowRequestsSerializer

context = 'localhost:8000/'

import uuid
def uuidGenerator():
    result = uuid.uuid4()
    return result.hex

def getCurrentDate():
    return datetime.today().strftime('%Y-%m-%dT%H:%M:%S')

#create a generalized object that allows for sorting based on date published
class DjangoObj:
    def __init__(self, obj, data):
        self.obj = obj
        self.date = obj.published
        self.data = data

    def __lt__(self, other):
        return self.date < other.date

class PostsAPIs(viewsets.ViewSet):

    #GET authors/{AUTHOR_ID/posts/{POST_ID}
    #get the public post whose id is POST_ID
    @action(detail=True, methods=['get'],)
    def getPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        try:
            post = Posts.objects.get(author = authorId, id = postId, visibility = Posts.PUBLIC)
        except Posts.DoesNotExist:
            post = None
        serializer = PostsSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)

    #POST authors/{AUTHOR_ID/posts/{POST_ID}
    #update the post whose id is POST_ID (must be authenticated)
    @action(detail=True, methods=['post'],)
    def updatePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        body = JSONParser().parse(io.BytesIO(request.body))
        post = Posts.objects.get(author = authorId, id = postId, visibility = Posts.PUBLIC)
        editableColumns = ["title", "description", "content"]
        edited = False
        for key, value in body.items():
            if key in editableColumns:
                setattr(post, key, value)
                edited = True
        if edited: post.save()
        return Response({"Success"}, status=status.HTTP_200_OK)

    #DELETE authors/{AUTHOR_ID/posts/{POST_ID}
    #remove the post whose id is POST_ID
    @action(detail=True, methods=['delete'],)
    def deletePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        Posts.objects.get(author = authorId, id = postId, visibility = Posts.PUBLIC).delete()
        return Response({"Success"}, status=status.HTTP_200_OK)

    #PUT authors/{AUTHOR_ID/posts/{POST_ID}
    #create a post where its id is POST_ID
    @action(detail=True, methods=['put'],)
    def createPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        body = defaultdict(lambda: None, JSONParser().parse(io.BytesIO(request.body)))
        post = Posts.objects.create(
            id = postId,
            type = body['type'],
            title = body['title'],
            source = body['source'],
            origin = body['origin'],
            description = body['description'],
            contentType = body['contentType'],
            content = body['content'],
            originalAuthor = Authors.objects.get(id = body['originalAuthor']),
            author = Authors.objects.get(id = authorId),
            published = body['published'],
            visibility = body['visibility'],
            unlisted = body['unlisted']
        )
        serializer = PostsSerializer(post)
        return Response(serializer.data)

    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/image
    #get the public post converted to binary as an image
    @action(detail=True, methods=['get'],)
    def getImagePost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]
        queryset = Posts.objects.raw("""
            YOUR SQL HERE
        """)
        
        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)

#completed and tested
class CommentsAPIs(viewsets.ViewSet):

    #TESTED
    #
    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    #get the list of comments of the post whose id is POST_ID
    @action(detail=True, methods=['get'],)
    def getComments(self, request, *args, **kwargs):
        postId = kwargs["postId"]
        queryset = Comments.objects.filter(post_id=postId).order_by('-published')
        
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)

    #TESTED
    #
    #POST authors/{AUTHOR_ID}/posts/{POST_ID}/comments
    #if you post an object of “type”:”comment”, it will add your comment to the post whose id is POST_ID
    @action(detail=True, methods=['post'],)
    def createComment(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]

        #check that authorId and postId exist
        if not Authors.objects.filter(id=authorId).count() ==1:
            return Response({"Tried to send post to non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to send non-existent post"}, status=status.HTTP_400_BAD_REQUEST)

        author = Authors.objects.get(id=authorId)
        post = Posts.objects.get(id=postId)

        #check that contentType is a valid choice
        body = JSONParser().parse(io.BytesIO(request.body))
        contentType = 'text/plain'
        if 'contentType' in body:
            if body['contentBody'] == 'text/markdown':
                contentType = 'text/markdown'
            elif body['contentBody'] != 'text/plain':
                return Response({"Failed comment creation. Invalid input for contentBody."}, status=status.HTTP_400_BAD_REQUEST)

        if 'comment' in body:
            comment = str(body['comment'])
        else:
            return Response({"Failed comment creation. Missing 'comment' column."}, status=status.HTTP_400_BAD_REQUEST)

        Comments.objects.create(
            id = uuidGenerator(),
            author = author,
            post = post,
            contentType = contentType,
            comment = comment
        )

        return Response({"Comment Created Successfully"}, status=status.HTTP_200_OK)

#completed and tested
class LikesAPIs(viewsets.ViewSet):

    #TESTED
    #
    #POST authors/{AUTHOR_ID}/posts/{POST_ID}/likes/{LIKER_ID}
    @action(detail=True, methods=['post'])
    def createPostLike(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        postId = kwargs["postId"]
        
        #check that authorId and postId exist
        if Authors.objects.filter(id=likerId).count() < 1:
            return Response({"Tried to check likes of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if Posts.objects.filter(id=postId).count() < 1:
            return Response({"Tried to check likes on a non-existent post"}, status=status.HTTP_400_BAD_REQUEST)

        liker = Authors.objects.get(id=likerId)
        post = Posts.objects.get(id=postId)
        if Likes.objects.filter(post=post, author=liker).count() >= 1:
            return Response({"Tried to like a post you've already liked"}, status=status.HTTP_400_BAD_REQUEST)

        Likes.objects.create(
            id = uuidGenerator(),
            context = context,
            summary = "{liker.displayName} Likes your post",
            author = liker,
            post = post
        )

        return Response("{Like created successfully}", status=status.HTTP_200_OK )

    #TESTED
    #
    #DELETE authors/{AUTHOR_ID}/posts/{POST_ID}/likes/{LIKER_ID}
    @action(detail=True, methods=['delete'])
    def deletePostLike(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        postId = kwargs["postId"]
        
        #check that authorId and postId exist
        if Authors.objects.filter(id=likerId).count() < 1:
            return Response({"Tried to delete a like of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if Posts.objects.filter(id=postId).count() < 1:
            return Response({"Tried to delete a like on a non-existent post"}, status=status.HTTP_400_BAD_REQUEST)
        liker = Authors.objects.get(id=likerId)
        post = Posts.objects.get(id=postId)
        
        Likes.objects.filter(post=post, author=liker).delete()
        
        return Response({"Delete Like Successful"}, status=status.HTTP_200_OK)


    #TESTED
    #
    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/likes/inbox?page=value&size=value
    #a list of likes from other authors on AUTHOR_ID’s post POST_ID
    @action(detail=True, methods=['get'],)
    def getPostLikes(self, request, *args, **kwargs):
        postId = kwargs["postId"]
        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )
            
        likeObjs = []
        for like in Likes.objects.filter(post_id=postId):
            likeObjs.append(DjangoObj(like, LikesSerializer(like, many=False).data))

        likeObjs.sort()
        output = []
        for likeObjIdx in range((page-1)*size, page*size):
            if likeObjIdx >= len(likeObjs):
                break
            output.append(likeObjs[likeObjIdx].data)   
        
        return Response(output, status=status.HTTP_200_OK)

    #TESTED
    #
    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes/inbox?page=value&size=value
    #a list of likes from other authors on AUTHOR_ID’s post POST_ID comment COMMENT_ID
    @action(detail=True, methods=['get'],)
    def getCommentLikes(self, request, *args, **kwargs):
        commentId = kwargs["commentId"]
        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )

        commentLikeObjs = []
        for like in LikesComments.objects.filter(comment_id=commentId):
            commentLikeObjs.append(DjangoObj(like, LikesCommentsSerializer(like, many=False).data))

        commentLikeObjs.sort()
        output = []
        for commentLikeObjIdx in range((page-1)*size, page*size):
            if commentLikeObjIdx >= len(commentLikeObjs):
                break
            output.append(commentLikeObjs[commentLikeObjIdx].data)   
        
        return Response(output, status=status.HTTP_200_OK)

#completed and tested
class LikedAPIs(viewsets.ViewSet):
    #TESTED
    #
    #GET authors/{AUTHOR_ID}/posts/{POST_ID}/like/{LIKER_ID}
    #returns true if authorId has made a like on postId, otherwise false
    @action(detail=True, methods=['get'])
    def getAuthorPostLiked(self, request, *args, **kwargs):
        likerId = kwargs["likerId"]
        postId = kwargs["postId"]
        
        #check that authorId and postId exist
        if not Authors.objects.filter(id=likerId).count() == 1:
            return Response({"Tried to check likes of a non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to check likes on a non-existent post"}, status=status.HTTP_400_BAD_REQUEST)

        liker = Authors.objects.get(id=likerId)
        post = Posts.objects.get(id=postId)

        if Likes.objects.filter(post=post, author=liker).count() >= 1:
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_200_OK)

    #TESTED
    #
    #GET authors/{AUTHOR_ID}/liked/inbox?page=value&size=value
    #list what public things AUTHOR_ID liked
    @action(detail=True, methods=['get'],)
    def getAuthorLiked(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )

        likeObjs = []
        for like in Likes.objects.filter(author_id=authorId):
            likeObjs.append(DjangoObj(like, LikesSerializer(like, many=False).data))
        for commentLike in LikesComments.objects.filter(author_id=authorId):
            likeObjs.append(DjangoObj(commentLike, LikesCommentsSerializer(commentLike, many=False).data))

        likeObjs.sort()
        output = []
        for likeObjIdx in range((page-1)*size, page*size):
            if likeObjIdx >= len(likeObjs):
                break
            output.append(likeObjs[likeObjIdx].data)   
        
        return Response(output, status=status.HTTP_200_OK)

#completed and tested
class InboxAPIs(viewsets.ViewSet):

    #TESTED
    #
    #GET authors/{AUTHOR_ID}/inbox?page=value&size=value
    #if authenticated get a list of posts sent to AUTHOR_ID (paginated)
    @action(detail=True, methods=['get'],)
    def getInbox(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        try:
            page = int(request.GET.get('page',1))
            size = int(request.GET.get('size',10))
        except:
            return Response("{Page or Size not an integer}", status=status.HTTP_400_BAD_REQUEST )

        inboxObjs = []
        #get enough posts, sorted
        for inbox in Inbox.objects.filter(author_id=authorId):
            post = Posts.objects.get(id=inbox.post_id)
            inboxObjs.append(DjangoObj(post, PostsSerializer(post, many=False).data))

            #get enough likes, sorted
            for like in Likes.objects.filter(post_id=post.id):
                inboxObjs.append(DjangoObj(like, LikesSerializer(like, many=False).data))

            #get enough comments, sorted
            for comment in Comments.objects.filter(post_id=post.id):
                inboxObjs.append(DjangoObj(comment, CommentsSerializer(comment, many=False).data))
                for commentLike in LikesComments.objects.filter(comment_id=comment.id):
                    inboxObjs.append(DjangoObj(commentLike, LikesCommentsSerializer(commentLike, many=False).data))
        #paginate
        inboxObjs.sort()
        output = []
        for inboxObjIdx in range((page-1)*size, page*size):
            if inboxObjIdx >= len(inboxObjs):
                break
            output.append(inboxObjs[inboxObjIdx].data)       

        if len(inboxObjs) == 0:
            return Response("{Nothing to show}", status=status.HTTP_200_OK )

        return Response(output, status=status.HTTP_200_OK)

    #TESTED
    #
    #POST authors/{AUTHOR_ID}/inbox + /{POST_ID}
    #send a post to the author
    @action(detail=True, methods=['post'],)
    def sendPost(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        postId = kwargs["postId"]

        #check that authorId and postId exist
        if not Authors.objects.filter(id=authorId).count() ==1:
            return Response({"Tried to send post to non-existent author"}, status=status.HTTP_400_BAD_REQUEST)
        if not Posts.objects.filter(id=postId).count() == 1:
            return Response({"Tried to send non-existent post"}, status=status.HTTP_400_BAD_REQUEST)

        author = Authors.objects.get(id=authorId)
        post = Posts.objects.get(id=postId)
        Inbox.objects.create(
            id = uuidGenerator(),
            author = author,
            post = post
        )

        return Response({"Post Sent to Inbox Successfully"}, status=status.HTTP_200_OK)

    #TESTED
    #
    #DELETE authors/{AUTHOR_ID}/inbox
    #clear the inbox
    @action(detail=True, methods=['delete'],)
    def deleteInbox(self, request, *args, **kwargs):
        authorId = str(kwargs["authorId"])
        if not Authors.objects.filter(id=authorId).count() == 1:
            return Response({"This Author does not exist"}, status=status.HTTP_404_NOT_FOUND)

        authorObj = Authors.objects.get(id=authorId)
        Inbox.objects.filter(author=authorObj).delete()
        
        return Response({"Delete Inbox Successful"}, status=status.HTTP_200_OK)

class FollowRequestsAPIs(viewsets.ViewSet):

    #GET authors/{AUTHOR_ID}/followRequest
    #get all the people who want to follow AUTHOR_ID
    @action(detail=True, methods=['get'],)
    def getFollowRequests(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        try:
            requestFollowers = FollowRequests.objects.filter(receiver=authorId)
        except FollowRequests.DoesNotExist:
            requestFollowers = None
        serializer = FollowRequestsSerializer(requestFollowers, many=True)
        return Response(serializer.data)

    #DELETE authors/{AUTHOR_ID}/followRequest/{FOREIGN_AUTHOR_ID}
    #remove FOREIGN_AUTHOR_ID's request to follow AUTHOR_ID (when AUTHOR_ID approve/deny a request)
    @action(detail=True, methods=['delete'],)
    def removeRequest(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        try:
            requestFollowers = FollowRequests.objects.get(receiver=authorId, requester=foreignAuthorId)
            requestFollowers.delete()
        except FollowRequests.DoesNotExist:
            requestFollowers = None
        serializer = FollowersSerializer(requestFollowers)
        return Response(serializer.data)

    #GET authors/{AUTHOR_ID}/followRequest/{FOREIGN_AUTHOR_ID}
    #check if FOREIGN_AUTHOR_ID has requested to follow AUTHOR_ID
    @action(detail=True, methods=['get'],)
    def checkRequestedToFollow(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        try:
            followRequested = FollowRequests.objects.get(receiver=authorId, requester=foreignAuthorId)
        except FollowRequests.DoesNotExist:
            followRequested = None
        serializer = FollowRequestsSerializer(followRequested)
        return Response(serializer.data)

    #POST authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #create AUTHOR_ID request to follow FOREIGN_AUTHOR_ID
    @action(detail=True, methods=['post'],)
    def requestToFollow(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        if not FollowRequests.objects.filter(requester=authorId, receiver=foreignAuthorId).count() == 0:
            return Response({"Failed to send a request to follow as a request to follow already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        FollowRequests.objects.create(
            id = uuidGenerator(),
            requester = Authors.objects.get(id = authorId),
            receiver = Authors.objects.get(id = foreignAuthorId)
        )
        return Response({"Request to follow Successful"}, status=status.HTTP_200_OK)
    
class FollowsAPIs(viewsets.ViewSet):

    #GET authors/{AUTHOR_ID}/followers
    #get all the followers of AUTHOR_ID
    @action(detail=True, methods=['get'],)
    def getFollowers(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        try:
            followers = Followers.objects.filter(followed=authorId)
        except Followers.DoesNotExist:
            followers = None
        serializer = FollowersSerializer(followers, many=True)
        return Response(serializer.data)
    
    #GET authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #check if FOREIGN_AUTHOR_ID is following AUTHOR_ID
    @action(detail=True, methods=['get'],)
    def checkFollower(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        try:
            follower = Followers.objects.get(followed=authorId, follower=foreignAuthorId)
        except Followers.DoesNotExist:
            follower = None
        serializer = FollowersSerializer(follower)
        return Response(serializer.data)

    #PUT authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    @action(detail=True, methods=['put'],)
    def addFollower(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        if not FollowRequests.objects.filter(receiver=authorId, requester=foreignAuthorId).count() == 1:
            return Response({"Failed to add a follower. The other party hasn't requested to follow you"}, status=status.HTTP_400_BAD_REQUEST)
        Followers.objects.create(
            id = uuidGenerator(),
            followed = Authors.objects.get(id = authorId),
            follower = Authors.objects.get(id = foreignAuthorId)
        )

        FollowRequests.objects.get(receiver=authorId, requester=foreignAuthorId).delete()
        return Response({"Add a follower Successful"}, status=status.HTTP_200_OK)

    #DELETE authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
    @action(detail=True, methods=['delete'],)
    def removeFollower(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]
        foreignAuthorId = kwargs["foreignAuthorId"]
        try:
            follower = Followers.objects.get(followed=authorId, follower=foreignAuthorId)
            follower.delete()
        except Followers.DoesNotExist:
            return Response({"Failed to remove follower. You need to follow them first before you can unfollow them"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Remove follower Successful"}, status=status.HTTP_200_OK)
    
    #POST authors/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    #create FOREIGN_AUTHOR_ID's request to follow AUTHOR_ID
    @action(detail=True, methods=['post'],)
    def requestToFollow(self, request, *args, **kwargs):
        return FollowRequestsAPIs.requestToFollow(self, request, *args, **kwargs)

class AuthorsAPIs(viewsets.ViewSet):

    generic_profile_image_path = '../images/generic_profile_image.png'
    
    #TESTED
    #GET //service/authors/{AUTHOR_ID}
    @action(detail=True, methods=['get'])
    def getAuthor(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]

        author = Authors.objects.filter(id=authorId)
        # Since id is the primary key of the Author table, there can only be 0 ot
        # 1 authors with this id
        if author.count() == 0:
            return Response("Author does not exist", status=status.HTTP_404_NOT_FOUND)
        
        author = author.get(id=authorId)

        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)
    
    #TESTED
    #GET //service/find?query={SEARCH_QUERY}&page={PAGE_NUM}&size={PAGE_SIZE}
    @action(detail=True, methods=['get'])
    def searchForAuthors(self, request, *args, **kwargs):
        #We search for displayName matching search_query
        search_query = request.GET.get('query')
        page_num = request.GET.get('page', 1)
        page_size = request.GET.get('size', 10)

        authors = Authors.objects.filter(displayName__contains=search_query)
        paginator = Paginator(authors, page_size)
        page_obj = paginator.page(page_num)
        serializer = AuthorSerializer(page_obj, many=True)
        print(serializer.data)
        return Response(serializer.data)

    #TESTED
    #GET //service/authors?page={PAGE_NUM}&size={PAGE_SIZE}
    @action(detail=True, methods=['get'])
    def getAuthors(self, request, *args, **kwargs):
        page_num = request.GET.get('page', 1)
        page_size = request.GET.get('size', 10)

        authors = Authors.objects.all()
        paginator = Paginator(authors, page_size)
        page_obj = paginator.page(page_num)
        serializer = AuthorSerializer(page_obj, many=True)
        print(serializer.data)
        res = Response(serializer.data)
        return res

   
    #POST //service/authors/{AUTHOR_ID}
    @action(detail=True, methods=['post'])
    def modifyAuthor(self, request, *args, **kwargs):
        authorId = kwargs["authorId"]

        author = Authors.objects.filter(id=authorId)
        # Since id is the primary key of the Author table, there can only be 0 ot
        # 1 authors with this id
        if author.count() == 0:
            return Response("Author does not exist!", status=status.HTTP_404_NOT_FOUND)
        author = author.get(id=authorId)

        request_body = request.POST
        if len(request_body) == 0:
            return Response("Empty POST body. Did you mean GET?", status=status.HTTP_400_BAD_REQUEST)

        editable_fields = ["github", "profileImage"]
        for field in request_body.keys():
            if field not in editable_fields:
                return Response("Problem with POST. Aborting!", status=status.HTTP_400_BAD_REQUEST)
        
        for field, value in request_body.items():
            if field == "profileImage":
                if value.strip() == "":
                    value = request.build_absolute_uri(self.generic_profile_image_path)
            if field == "github" and value.strip() == "":
                value = None
            setattr(author, field, value)

        author.save()

        return Response("Modified Author successfully")
    
    #PUT //service/authors
    @action(detail=True, methods=['put'])
    def createAuthor(self, request, *args, **kwargs):
        
        request_body = request.POST

        authorId = uuidGenerator()
        host = request.build_absolute_uri().split('/authors/')[0]
        if "displayName" in request_body and request_body["displayName"].strip() != "":
            author = Authors.objects.filter(displayName=request_body["displayName"])
            if author.count() == 1:
                return Response("Display name already exists!", status=status.HTTP_409_CONFLICT)
            displayName = request_body['displayName']
        else:
            return Response("Can't create a profile with no display name!", status=status.HTTP_400_BAD_REQUEST)
        url = host + '/authors/' + authorId
        profileImage = request.build_absolute_uri(self.generic_profile_image_path) 
        github = request_body["github"] if "github" in request_body.items() and request_body["github"].strip() != "" else None

        author = Authors.objects.create(id=authorId, host=host, displayName=displayName, url=url, accepted=False, github=github, profileImage=profileImage)

        author.save()

        return Response("Created Author successfully", status=status.HTTP_200_OK)

         



    
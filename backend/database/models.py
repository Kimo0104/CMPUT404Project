from django.db import models

class Authors(models.Model):
    id = models.CharField(max_length = 255, primary_key = True)
    type = models.CharField(max_length = 255, default = "author")
    host = models.CharField(max_length = 255)
    displayName = models.CharField(max_length = 32)
    url = models.CharField(max_length = 255)
    github = models.CharField(max_length = 255, null=True)
    accepted = models.BooleanField(default = False)
    profileImage = models.CharField(max_length = 255)

class Posts(models.Model):
    PLAINTEXT = 'text/plain'
    MARKDOWN = 'text/markdown'
    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIENDS'
    UNLISTED = 'UNLISTED'
    content_type_choices = [
        (PLAINTEXT, 'PLAINTEXT'),
        (MARKDOWN, 'COMMONMARK')
    ]
    visibility_choices = [
        (PUBLIC, 'PUBLIC'),
        (FRIENDS, 'FRIENDS'),
        (UNLISTED, 'UNLISTED')
    ]
    id = models.CharField(max_length = 255, primary_key = True)
    type = models.CharField(max_length = 255, default = "post")
    title = models.CharField(max_length = 255)
    source = models.CharField(max_length = 255)
    origin = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    contentType = models.CharField(max_length = 15, choices = content_type_choices, default = PLAINTEXT)
    content = models.TextField()
    originalAuthor = models.ForeignKey(Authors, on_delete = models.DO_NOTHING, related_name = "originalPoster")
    author = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "poster")
    count = models.IntegerField(default = 0)
    published = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length = 8, choices = visibility_choices, default = PUBLIC)


class Followers(models.Model):
    id = models.CharField(max_length = 255, primary_key = True)
    followed = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "follower")
    follower = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name="followed")


class FollowRequests(models.Model):
    id = models.CharField(max_length = 255, primary_key = True)
    receiver = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "receiver")
    requester = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "requester")


class Comments(models.Model):
    PLAINTEXT = 'text/plain'
    MARKDOWN = 'text/markdown'
    choices = [
        (PLAINTEXT, 'PLAINTEXT'),
        (MARKDOWN, 'MARKDOWN')
    ]
    id = models.CharField(max_length=255, primary_key = True)
    type = models.CharField(max_length=16, default = "comment")
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
    comment = models.CharField(max_length=255)
    contentType = models.CharField(
        max_length = 15,
        choices = choices,
        default = PLAINTEXT
    )
    published = models.DateTimeField(auto_now_add = True)

class Likes(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    context = models.CharField(max_length=255)
    summary = models.CharField(max_length=64)
    type = models.CharField(max_length=16, default = "like")
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)

class LikesComments(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    context = models.CharField(max_length=255)
    summary = models.CharField(max_length=64)
    type = models.CharField(max_length=16, default = "likescomment")
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete = models.CASCADE)

class Inbox(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
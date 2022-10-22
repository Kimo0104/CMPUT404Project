from django.db import models

class Authors(models.Model):
    id = models.CharField(max_length = 255, primary_key = True)
    type = models.CharField(max_length = 255, default = "author", blank=True, null = True)
    host = models.CharField(max_length = 255)
    displayName = models.CharField(max_length = 32)
    url = models.CharField(max_length = 255)
    github = models.CharField(max_length = 255)
    accepted = models.BooleanField(blank = True, default = True, null = True)
    profileImage = models.CharField(max_length = 255)

class Posts(models.Model):
    PLAINTEXT = 'text/plain'
    MARKDOWN = 'text/markdown'
    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIENDS'
    content_type_choices = [
        (PLAINTEXT, 'PLAINTEXT'),
        (MARKDOWN, 'COMMONMARK')
    ]
    visibility_choices = [
        (PUBLIC, 'PUBLIC'),
        (FRIENDS, 'FRIENDS')
    ]
    id = models.CharField(max_length = 255, primary_key = True)
    type = models.CharField(max_length = 255, default = "post", blank=True, null = True)
    title = models.CharField(max_length = 255)
    source = models.CharField(max_length = 255)
    origin = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    contentType = models.CharField(max_length = 15, choices = content_type_choices, default = PLAINTEXT, blank = True, null = True)
    content = models.TextField()
    author = models.ForeignKey(Authors, on_delete= models.CASCADE)
    count = models.IntegerField(default = 0, blank = True, null = True)
    published = models.DateTimeField(auto_now_add=True, blank=True, null = True)
    visibility = models.CharField(max_length = 8, choices = visibility_choices, default = PUBLIC, null = True, blank = True)
    unlisted = models.BooleanField(default = False, blank = True, null = True)


class Followers(models.Model):
    id = models.CharField(max_length = 255, primary_key = True)
    followed = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "follower")
    follower = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name="followed")


class FollowRequests(models.Model):
    id = models.CharField(max_length = 255, primary_key = True)
    reciever = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "reciever")
    requester = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "requester")


class Comments(models.Model):
    PLAINTEXT = 'text/plain'
    MARKDOWN = 'text/markdown'
    choices = [
        (PLAINTEXT, 'PLAINTEXT'),
        (MARKDOWN, 'MARKDOWN')
    ]
    id = models.CharField(max_length=255, primary_key = True)
    type = models.CharField(max_length=16, default = "comment", blank=True, null = True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
    comment = models.CharField(max_length=255)
    contentType = models.CharField(
        max_length = 15,
        choices = choices,
        default = PLAINTEXT, 
        blank = True, 
        null = True
    )
    published = models.DateTimeField(auto_now_add=True, blank=True)

class Likes(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    context = models.CharField(max_length=255)
    summary = models.CharField(max_length=64)
    type = models.CharField(max_length=16, default = "like", blank = True, null = True)
    published = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)

class LikesComments(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    context = models.CharField(max_length=255)
    summary = models.CharField(max_length=64)
    type = models.CharField(max_length=16, default = "likescomment", blank=True, null = True)
    published = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete = models.CASCADE)

class Liked(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    like = models.ForeignKey(Likes, on_delete = models.CASCADE)

class Inbox(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)
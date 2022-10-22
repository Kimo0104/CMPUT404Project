from django.db import models

class Authors(models.Model):
    id = models.CharField(max_length = 255, primary_key = True)
    type = models.CharField(max_length = 255, default = "author")
    host = models.CharField(max_length = 255)
    dispayName = models.CharField(max_length = 32)
    url = models.CharField(max_length = 255)
    github = models.CharField(max_length = 255)
    accepted = models.BooleanField(default = True)
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
    type = models.CharField(max_length = 255, default = "author")
    title = models.CharField(max_length = 255)
    source = models.CharField(max_length = 255)
    origin = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    contentType = models.CharField(max_length = 15, choices = content_type_choices, default = PLAINTEXT, blank = True, null = True)
    content = models.TextField()
    author = models.ForeignKey(Authors, on_delete= models.CASCADE)
    count = models.IntegerField(default = 0)
    comments = models.CharField(max_length = 255)
    published = models.DateTimeField()
    visibility = models.CharField(max_length = 8, choices = visibility_choices, default = PUBLIC)
    unlisted = models.BooleanField(default = False)


class Followers(models.Model):
    followed = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "follower")
    follower = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name="followed")


class FollowRequest(models.Model):
    reciever = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "reciever")
    requester = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "requester")


class Comments(models.Model):
    PLAINTEXT = 'PT'
    MARKDOWN = 'CM'
    choices = [
        (PLAINTEXT, 'PLAINTEXT'),
        (MARKDOWN, 'MARKDOWN')
    ]
    id = models.CharField(max_length=255, primary_key = True)
    type = models.CharField(max_length=16)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    comment = models.CharField(max_length=255)
    contentType = models.CharField(
        max_length = 2,
        choices = choices,
        default = PLAINTEXT, 
        blank = True, 
        null = True
    )
    published = models.DateField()

class Likes(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    context = models.CharField(max_length=255)
    summary = models.CharField(max_length=64)
    type = models.CharField(max_length=16)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)

class Liked(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    like = models.ForeignKey(Likes, on_delete = models.CASCADE)

class Inbox(models.Model):
    id = models.CharField(max_length=255, primary_key = True)
    author = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete = models.CASCADE)
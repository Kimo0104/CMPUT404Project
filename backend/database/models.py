from django.db import models

class Authors(models.Model):
    host = models.CharField(max_length=255)
    display_name = models.CharField(max_length=32)
    github_url = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    accepted = models.BooleanField()

class Posts(models.Model):
    PLAINTEXT = 'PT'
    COMMONMARK = 'CM'
    choices = [
        (PLAINTEXT, 'PLAINTEXT'),
        (COMMONMARK, 'COMMONMARK')
    ]
    title = models.CharField(max_length = 64)
    description_type = models.CharField(
        max_length = 2,
        choices = choices,
        default = PLAINTEXT
    )
    description = models.TextField()
    date = models.DateField()
    image_url = models.CharField(max_length=255)
    author = models.ForeignKey(Authors, on_delete= models.CASCADE)

class Comments(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)

class Likes(models.Model):
    liker = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)

class Follows(models.Model):
    PENDING = 0
    FOLLOWING = 1
    choices = [
        (PENDING, 'Pending') ,
        (FOLLOWING, 'Following')   
    ]
    relationship_state = models.IntegerField(
        choices = choices,
        default = PENDING
    )
    author = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name = "follower")
    foreign_author = models.ForeignKey(Authors, on_delete= models.CASCADE, related_name="followed")


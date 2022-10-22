from django.db import models

class Authors(models.Model):
    id = models.CharField(max_length = 255, primary_key = True)
    type = models.CharField(max_length = 255, default = "author")
    host = models.CharField(max_length = 255)
    name = models.CharField(max_length = 32)
    url = models.CharField(max_length = 255)
    github = models.CharField(max_length = 255)
    accepted = models.BooleanField(default = True)
    profile_image = models.CharField(max_length = 255)

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
    content_type = models.CharField(max_length = 15, choices = content_type_choices, default = PLAINTEXT, blank = True, null = True)
    content = models.TextField()
    author = models.ForeignKey(Authors, on_delete= models.CASCADE)
    count = models.IntegerField(default = 0)
    comments = models.CharField(max_length = 255)
    published = models.DateTimeField()
    visibility = models.CharField(max_length = 8, choices = visibility_choices, default = PUBLIC)
    unlisted = models.BooleanField(default = False)


class Comments(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(Authors, on_delete = models.CASCADE)
    post = models.ForeignKey(Posts, on_delete = models.CASCADE)


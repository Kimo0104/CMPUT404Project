from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Authors)
admin.site.register(Posts)
admin.site.register(Followers)
admin.site.register(FollowRequests)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(LikesComments)
admin.site.register(Liked)
admin.site.register(Inbox)

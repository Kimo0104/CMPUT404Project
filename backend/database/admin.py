from django.contrib import admin
from .models import Authors, Posts, Followers, FollowRequests, Comments, Likes, LikesComments, Inbox

@admin.action(description='Mark selected users as accepted')
def make_accepted(modeladmin, request, queryset):
    queryset.update(accepted=True)

class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['displayName']
    list_filter = ['accepted']
    actions = [make_accepted]


admin.site.register(Authors, AuthorsAdmin)
admin.site.register(Posts)
admin.site.register(Followers)
admin.site.register(FollowRequests)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(LikesComments)
admin.site.register(Inbox)

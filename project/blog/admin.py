from django.contrib import admin

from blog.models import *

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Unlike)
admin.site.register(CommentLiked)
admin.site.register(CommentUnliked)

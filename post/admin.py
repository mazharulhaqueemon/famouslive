from django.contrib import admin
from .models import post,PostImage,PostVideo,Like

admin.site.register(post)
admin.site.register(PostImage)
admin.site.register(PostVideo)
admin.site.register(Like)

# Register your models here.

from django.contrib import admin
from .models import User, Post, PostImage, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)


class PostImageAdmin(admin.StackedInline):
    model = PostImage
    extra = 1
    max_num = 4

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
        model = Post

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass
 
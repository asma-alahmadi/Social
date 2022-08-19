from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


# Create your models here.

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add= True)
    likes = models.ManyToManyField(User, related_name="likes", null=True, blank=True)

    class Meta:
        ordering = ['-date',] 

    def serialize(self):
        return {
            "id": self.id,
            "post": self.post,
            "likes": [user.post for user in self.likes.all()]
        }
        
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    imgs = models.FileField(blank=True, null=True, upload_to="images/" )

    def save(self, *args, **kwargs):
        if self.imgs:
            super().save(*args, **kwargs)
        img = Image.open(self.imgs.path)
        if img.height > 400 or img.width > 400:
            output_size = (400,400)
            img.thumbnail(output_size)
            img.save(self.imgs.path)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=300)
    comment_date = models.DateTimeField(auto_now_add= True)
    comment_like = models.ManyToManyField(User, related_name="com_like", null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "com_like": [user.comment for user in self.comment_like.all()]
        }

    def __str__(self):
        return f"{self.user} adds comment to post number {self.post.id}"
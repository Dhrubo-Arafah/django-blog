from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField(max_length=265, verbose_name="Put a title")
    slug = models.SlugField(max_length=265, unique=True)
    content = models.TextField(verbose_name="What's on your mind?")
    cover = models.ImageField(upload_to='blog_image', verbose_name="Image")
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.user + "Comment on" + self.comment


class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_liked')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_liked')

    def __str__(self):
        return self.user + "liked" + self.blog


class Unlike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_unliked')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_unliked')

    def __str__(self):
        return self.user + "Unliked" + self.blog


class CommentLiked(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_liked')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_liked')

    def __str__(self):
        return self.user + "Liked Comment of" + self.comment


class CommentUnliked(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_unliked')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_unliked')

    def __str__(self):
        return self.user + "unliked Comment of" + self.comment

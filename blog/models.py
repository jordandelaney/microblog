from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from microblog.settings import AUTH_USER_MODEL
from django.template.defaultfilters import slugify
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
class BlogPost(models.Model):
    """Model representing a blog post"""
    title = models.CharField(max_length=200, help_text="Enter a Title (Max 200 characters)")
    # Auto date add
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    # Foreign key to blogger - post can only belong to a blogger but a blogger can have multiple posts
    blogger = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Post content
    content = models.TextField(help_text="Enter your post here.")
    # Public content displayed outside your profile?
    private = models.BooleanField(default=False)
    # Slug for URLs
    slug = models.SlugField(default='', editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the url to access a detail view for this post"""
        return reverse('blog:post-detail', args=[self.pk,str(self.slug)])

    def is_new(self):
        """Determine if a post is new enough to get the New badge in sidebar"""
        return self.date_added > (timezone.now() - timedelta(days=1))

    def __str__(self):
        """Return a string representing BlogPost"""
        return f'{self.title} - {self.blogger.username}'

class Comment(models.Model):
    """Model representing a comment on a blog post"""
    # Auto date time add
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    # Foreign key to blog post - comment can only belong to a post but a post can have multiple comments
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    # Comment content
    comment = models.TextField(help_text='Enter your comment here.')
    # Comment owner - foreign key to user
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string of post title and username"""
        return f'Comment for "{self.post.title}" by {self.owner.username}'
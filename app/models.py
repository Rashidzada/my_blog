from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(blank=True)
    profile_pic = ProcessedImageField(
        upload_to='blog_images',
        processors=[ResizeToFit(width=800, height=600, upscale=False)],
        format='JPEG',
        options={'quality': 5},
        blank=True,
        null=True)

    def __str__(self) -> str:
        return f'{self.user.username}'
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    image = ProcessedImageField(
        upload_to='blog_images',
        processors=[ResizeToFit(width=800, height=600, upscale=False)],
        format='JPEG',
        options={'quality': 50},
        blank=True,
        null=True)
    youtube_link = models.CharField(max_length=200,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=55,blank=True,choices=(('submitted','submitted'),('rejected','rejected'),('reviewing','reviewing'),('accepted','accepted')),default='submitted')

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Profiles(models.Model):
   
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture =  models.ImageField(upload_to='App/social/profilePic/')
    cover=  models.ImageField(upload_to='App/social/coverPic/')
    # friends = models.ManyToManyField(User, related_name='user_friends')
    about = models.CharField(max_length=1000)
    phone = PhoneNumberField()
    follower = models.ManyToManyField(User, related_name='Profiles_followers', blank=True)
    country = CountryField()
    friends = models.ManyToManyField(User, related_name='user_friends')
    last_activity = models.DateTimeField(null=True, blank=True)
    # friend_requests = models.ManyToManyField(User,  related_name='received_friend_requests')
    # state = models.ForeignKey(Location,on_delete=models.CASCADE)
  
    def __str__(self) -> str:
        return f'{self.username}'
    


class Picture(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='App/pictures')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tagged_users = models.ManyToManyField(Profiles, related_name='picture_tagged_user')

class Tags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    tag_location = models.CharField(max_length=255)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='FriendRequests_sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='FriendRequests_recipient')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}"

class Chatt(models.Model):
    title = models.CharField(max_length=255)
    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    conversation  = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)
    timer = models.DateTimeField(auto_now_add=True)


































































# class Blog(models.Model):
#     username = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100) 
#     background_picture = models.ImageField(blank=True,default='Post/content.jpeg',upload_to='blogs/') 
#     body =  RichTextField()
#     slug = AutoSlugField(populate_from = 'title', unique=True)
#     category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='blog')
#     views = models.IntegerField(default=0)
#     # likes = models.IntegerField(default=0)
#     likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return str(self.title)
    
#     def get_absolut_url(self):
#         return reverse('Myapp:blog_title', args={self.slug, })
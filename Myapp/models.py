from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django_countries.fields import CountryField

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length = 15)
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self):
        return str(self.category)
    def get_absolut_url(self):
        return reverse('Myapp:category_filter', args={self.slug})
    
class Tag(models.Model):
    tag = models.CharField(max_length = 15)
    slug = AutoSlugField(populate_from = 'tag', unique=True)
    def __str__(self):
        return str(self.tag)
    def get_absolut_url(self):
        return reverse('Myapp:auto_filter', args={self.slug})
    
    
class Blog(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) 
    cover_picture = models.ImageField(blank=True,default='blogs/content.jpeg',upload_to='blogs/') 
    body =  RichTextField()
    slug = AutoSlugField(populate_from = 'title', unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='blog')
    views = models.IntegerField(default=0)
    # likes = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.title)
    
    def get_absolut_url(self):
        return reverse('Myapp:blog_title', args={self.slug, })
    
class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)    

    
class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    blog  =  models.ForeignKey(Blog,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=1000)
    
    def __str__(self):
        return str(self.username)
    
class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=25)
    message = models.TextField(max_length=1000)
    
    
class Question(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) 
    screenshot = models.ImageField(blank=True, default='/blogs/q.png',upload_to='question/') 
    body =  models.TextField(max_length=5000)
    slug = AutoSlugField(populate_from = 'title', unique=True, max_length=100)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.title)
    
    def get_absolut_url(self):
        return reverse('Myapp:question_title', args={self.slug, })


class Answer(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    question  =  models.ForeignKey(Question,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=1000)
    likes = models.IntegerField(default=0)
    liker = models.ManyToManyField(User, related_name='answer_likes')
    slug = models.SlugField(max_length=200, unique=True,null=True)
    class Meta:
        db_table = 'Myapp_answer'
    def __str__(self):
        return str(self.username)
    def total_likes(self):
        return self.liker.count()
    
class Like(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar =  models.ImageField(upload_to='profilePic/')
    bio = models.CharField(max_length=1000)
    phone = models.CharField(max_length=11)
    # country = CountryField()
    state = models.ForeignKey(Location,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.username}'
    



class LikeContent(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} likes {self.blog}"
    
class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
    
class Report(models.Model):
    class StatusChoices(models.TextChoices):
        Pending = "Pending"
        Inprogess = "in progress"
        Treated = "Treated"
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    culprit = models.CharField(max_length=20)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    screenshot = models.ImageField(blank=True,upload_to='report/')
    status = models.CharField(max_length=30, choices=StatusChoices.choices, default="Pending")

    def __str__(self) -> str:
        return f"{self.username} ------- {self.type} "
    

class Notification(models.Model):
    class StatusChoices(models.TextChoices):
        Read = "Read"
        Unread = "Unread"
    username = models.CharField(max_length=25)
    user = models.CharField(max_length=25)
    topic = models.CharField(max_length=25)
    notify = models.CharField(max_length=100)
    ids = models.CharField(max_length=100)
    isread = models.CharField(max_length=10, choices=StatusChoices.choices, default="Unread")
    
    def __str__(self) -> str:
        return f'notification for {self.username}'





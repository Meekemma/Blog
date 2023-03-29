from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
         return self.name
    
   


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    title=models.CharField(max_length=200, unique=True)
    slug=models.SlugField(max_length=200, unique=True)
    author=models.CharField(max_length=200, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image= models.ImageField(null=True, blank=True)

    class Meta:
        ordering =['-created_on']
   

    def __str__(self):
        return self.title
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url  = ''
        return url        
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": str(self.slug)})


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']


    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)  

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

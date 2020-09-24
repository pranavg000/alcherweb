from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class Tag(models.Model) :
    tag = models.CharField(default="",max_length=255)
    tag_id = models.AutoField(primary_key =True)



class BasePost(models.Model) :
    post_id = models.CharField(max_length=255)
    message = models.TextField(default="")
    description = models.TextField(default="")
    created_at = models.TextField(default ="")
    picture = models.URLField(blank=True)
    full_picture = models.URLField(blank=True)
    likes_cnt = models.IntegerField(default=0)
    shares_cnt = models.IntegerField(default=0)


class PagePost(BasePost) :
     tags = models.ManyToManyField(Tag,related_name="pageposts")
     liked_by = models.ManyToManyField(User,related_name ="liked_page_posts")
     from_name = models.TextField(default="")
     from_id = models.TextField(default="")

     


class UserSharedPost(BasePost) :
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="fbsharedposts")
    shared_post = models.ForeignKey(PagePost,on_delete=models.CASCADE,related_name="sharedposts")
    tags = models.ManyToManyField(Tag,related_name="usershares")
    likes_score = models.IntegerField(default= 0)
    tags_score = models.IntegerField(default = 0)
    shares_score = models.IntegerField(default = 0) 
    post_share_score = models.IntegerField(default = 0)
    parent_post_like_score = models.IntegerField(default = 0)

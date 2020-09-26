from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.




class Tag(models.Model) :
    tag = models.CharField(default="",max_length=255)
    tag_id = models.AutoField(primary_key =True)



class BasePost(models.Model) :
    post_id = models.CharField(max_length=255)
    created_at = models.TextField(default ="")
    likes_cnt = models.IntegerField(default=0)
    shares_cnt = models.IntegerField(default=0)


class PagePost(BasePost) :
     tags = models.ManyToManyField(Tag,related_name="pageposts")
     liked_by = models.ManyToManyField(User,related_name ="liked_page_posts")
     from_name = models.TextField(default="")
     from_id = models.TextField(default="")

     def __str__(self):
         return str(self.post_id)

     


class UserSharedPost(BasePost) :
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="fbsharedposts")
    shared_post = models.ForeignKey(PagePost,on_delete=models.CASCADE,related_name="sharedposts")
    tags = models.ManyToManyField(Tag,related_name="usershares")
    likes_score = models.IntegerField(default= 0)
    tags_score = models.IntegerField(default = 0)
    shares_score = models.IntegerField(default = 0) 
    post_share_score = models.IntegerField(default = 0)
    parent_post_like_score = models.IntegerField(default = 0)
    admin_approval = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        delta = 30
        if (self.post_share_score!=0) or (not self.admin_approval):
            delta = 0
        self.post_share_score+=delta
        self.user.ca_details.score+=delta
        super(UserSharedPost, self).save(*args, **kwargs) # Call the real save() method


    def __str__(self):
        return str(self.post_id)


@receiver(pre_delete,sender=UserSharedPost,dispatch_uid='shared_post_delete_signal')
def update_share_score(sender,instance,using,**kwargs):
    delta = 30
    if instance.post_share_score==0:
        delta=0
    instance.user.ca_details.score-=delta
    

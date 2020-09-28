from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from ca.scores import FB_SHARE_SCORE



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
        delta = FB_SHARE_SCORE                                                                                                                                      
        if (self.post_share_score!=0) or (not self.admin_approval):                                                                                                 
            delta = 0                                                                                                                                               
        self.post_share_score+=delta                                                                                                                                
        self.user.ca_details.score+=delta                                                                                                                           
        self.user.ca_details.fbscore+=delta                                                                                          
        super(UserSharedPost, self).save(*args, **kwargs) # Call the real save() method
                                                                                                                                                                                                                   
                                                                                                                                                                                                                   
    def __str__(self):                                                                                                                                                                                             
        return str(self.post_id)


class InviteAll(models.Model) :
    user = models.OneToOneField(User,on_delete =models.CASCADE ,related_name = "fb_invites_pic")
    image = models.ImageField(upload_to= "invitePics/" ,default = "") 
    invitesScore = models.IntegerField(default = 0)
    approval = models.IntegerField(default = 0)
    uploaded_at = models.DateField(auto_now = False,auto_now_add = True)
    triweekly_invite = models.IntegerField(default = 0)

    class Meta :
        ordering = ["-uploaded_at" ]



@receiver(pre_delete,sender=UserSharedPost,dispatch_uid='shared_post_delete_signal')
def update_share_score(sender,instance,using,**kwargs):
    instance.user.ca_details.score-=instance.post_share_score
    instance.user.ca_details.fbscore-=instance.post_share_score
    instance.user.ca_details.save()
    


class UserManualSharedPost(models.Model) :
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="fbmanualsharedposts")
    shared_post_url = models.URLField(max_length=1000)
    admin_approval = models.BooleanField(default=False)
    post_share_score = models.IntegerField(default= 0)


@receiver(pre_delete,sender=UserManualSharedPost,dispatch_uid='manual_shared_post_delete_signal')
def update_manual_share_score(sender,instance,using,**kwargs):
    instance.user.ca_details.score-=instance.post_share_score
    instance.user.ca_details.fbscore-=instance.post_share_score
    instance.user.ca_details.save()




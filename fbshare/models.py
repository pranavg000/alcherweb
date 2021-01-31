from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete,m2m_changed
from django.dispatch import receiver
from ca.scores import FB_SHARE_SCORE,FB_SHARED_POST_LIKES_SCORE,FB_SHARED_POST_SHARES_SCORE,FB_PARENT_POST_LIKE_SCORE



class Tag(models.Model) :
    tag = models.CharField(default="",max_length=255)
    tag_id = models.AutoField(primary_key =True)



class BasePost(models.Model) :
    post_id = models.CharField(max_length=255)
    created_at = models.TextField(default ="")
    likes_cnt = models.IntegerField(default=0)
    shares_cnt = models.IntegerField(default=0)


class PagePost(BasePost) :
     tags = models.ManyToManyField(Tag,related_name="pageposts",blank=True)
     liked_by = models.ManyToManyField(User,related_name ="liked_page_posts",blank=True)
     from_name = models.TextField(default="")
     from_id = models.TextField(default="")

     def __str__(self):
         return str(self.post_id)

     


class UserSharedPost(BasePost) :
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="fbsharedposts")
    shared_post = models.ForeignKey(PagePost,on_delete=models.CASCADE,related_name="sharedposts")
    tags = models.ManyToManyField(Tag,related_name="usershares",blank=True)
    likes_score = models.IntegerField(default= 0)
    tags_score = models.IntegerField(default = 0)
    shares_score = models.IntegerField(default = 0) 
    post_share_score = models.IntegerField(default = 0)
    triweekly_share = models.IntegerField(default = 0)
    admin_approval = models.BooleanField(default=True)
    def save(self, *args, **kwargs): 


        if self.admin_approval :
            delta_1 = FB_SHARE_SCORE
            delta_2 = FB_SHARED_POST_LIKES_SCORE
            delta_3 = FB_SHARED_POST_SHARES_SCORE

            
            

        else :
            delta_1 = 0
            delta_2 = 0
            delta_3 = 0


        self.user.ca_details.fbscore+=(delta_1-self.post_share_score)+(self.likes_cnt*delta_2-self.likes_score)+(self.shares_cnt*delta_3-self.shares_score )
        self.user.ca_details.score+=(delta_1-self.post_share_score)+(self.likes_cnt*delta_2-self.likes_score)+(self.shares_cnt*delta_3-self.shares_score )                                  
        self.user.ca_details.triweekly+=(delta_1-self.post_share_score)+(self.likes_cnt*delta_2-self.likes_score)+(self.shares_cnt*delta_3-self.shares_score )

        self.likes_score = self.likes_cnt*delta_2
        self.shares_score = self.shares_cnt*delta_3
        self.post_share_score=delta_1 

        self.triweekly_share = self.likes_score+self.shares_score+self.post_share_score


        
        
        super(UserSharedPost, self).save(*args, **kwargs)
        self.user.ca_details.save()# Call the real save() method
                                                                                                                                                                                                                   
                                                                                                                                                                                                                   
    def __str__(self):                                                                                                                                                                                             
        return str(self.post_id)


class InviteAll(models.Model) :
    user = models.OneToOneField(User,on_delete =models.CASCADE ,related_name = "fb_invites_pic")
    # image = models.ImageField(upload_to= "invitePics/" ,default = "") 
    invitesScore = models.IntegerField(default = 0)
    approval = models.IntegerField(default = 0)
    uploaded_at = models.DateField(auto_now = False,auto_now_add = True)
    triweekly_invite = models.IntegerField(default = 0)

    class Meta :
        ordering = ["-uploaded_at" ]



@receiver(pre_delete,sender=UserSharedPost,dispatch_uid='shared_post_delete_signal')
def update_share_score(sender,instance,using,**kwargs):
    instance.user.ca_details.score-=instance.post_share_score+instance.likes_score+instance.shares_score
    instance.user.ca_details.fbscore-=instance.post_share_score+instance.likes_score+instance.shares_score
    instance.user.ca_details.triweekly-=instance.post_share_score+instance.likes_score+instance.shares_score
    instance.user.ca_details.save()

@receiver(pre_delete,sender = PagePost ,dispatch_uid= 'page_post_delete_signail')
def change_like_score(sender,instance,using,**kwargs) :
    for u in instance.liked_by.all() :
        u.ca_details.fbscore-=FB_PARENT_POST_LIKE_SCORE
        u.ca_details.score-=FB_PARENT_POST_LIKE_SCORE
        u.ca_details.triweekly-=FB_PARENT_POST_LIKE_SCORE
        u.ca_details.save()
    


"""class UserManualSharedPost(models.Model) :
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name="fbmanualsharedposts")
    shared_post_url = models.URLField(max_length=1000)
    admin_approval = models.BooleanField(default=False)
    post_share_score = models.IntegerField(default= 0)


@receiver(pre_delete,sender=UserManualSharedPost,dispatch_uid='manual_shared_post_delete_signal')
def update_manual_share_score(sender,instance,using,**kwargs):
    instance.user.ca_details.score-=instance.post_share_score
    instance.user.ca_details.fbscore-=instance.post_share_score
    instance.user.ca_details.save()"""

def likedby_changed(sender,instance,action,pk_set,**kwargs) :
    ids = list(pk_set)
    user = User.objects.get(pk = ids[0])
    
    if action =="pre_add" :
        user.ca_details.fbscore+=FB_PARENT_POST_LIKE_SCORE
        user.ca_details.score+=FB_PARENT_POST_LIKE_SCORE
        user.ca_details.triweekly+=FB_PARENT_POST_LIKE_SCORE
    elif action =="pre_remove" :
        user.ca_details.fbscore-=FB_PARENT_POST_LIKE_SCORE
        user.ca_details.score-=FB_PARENT_POST_LIKE_SCORE
        user.ca_details.triweekly-=FB_PARENT_POST_LIKE_SCORE

    user.ca_details.save()

m2m_changed.connect(likedby_changed ,sender = PagePost.liked_by.through)


class InviteImage(models.Model) :
    invite = models.ForeignKey(InviteAll,on_delete =models.CASCADE ,related_name = "fb_images",)
    image = models.ImageField(upload_to= "invitePics/" ,default = "") 
    # invitesScore = models.IntegerField(default = 0)
    # approval = models.IntegerField(default = 0)
    # uploaded_at = models.DateField(auto_now = False,auto_now_add = True)
    # triweekly_invite = models.IntegerField(default = 0)
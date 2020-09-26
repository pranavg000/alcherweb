import facebook 
from django.contrib.auth.models import User 
from social_django.models import UserSocialAuth
from django.conf import settings
from fbshare.models import *




page_access_token ="EAANseDVfMw4BAJ8obz4y0Hm7yIW2vZBiiZARx9BC8tZBkEYq1ri1IXA6xaZAWSdw4w2kQjoodUe5brCmOVxBSU1VckkyqE60jLMOj6hsTB4AYSiM4DD3szT2siqgziJICTFjfYWYmdktQRtz9okBKzP3z2KZAAvJTgQFZC7ymsh11i9uZCR95lZB"
app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY 
app_secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET 
app_token = "963688477438734|QVCfBB1RC4ssBWVKQACXrio4ovI"




def get_page_posts() :
    api = facebook.GraphAPI(access_token=page_access_token ,version="2.12")
    page = api.get_object(id="101854044992923")
    posts = api.get_connections(id=page["id"] ,connection_name="posts",fields="id,message_tags,likes,shares,from,created_time")
    for post in posts["data"] :
    
        post_id = post["id"]
        print(post)
        P,created = PagePost.objects.get_or_create(post_id = post_id,from_name = post["from"]["name"],from_id= post["from"]["id"],created_at = post["created_time"])
        
        P.share_cnt = post["shares"]["count"] if "shares" in post.keys() else 0
        if "likes" in post.keys() :
          for like in post["likes"]["data"] :
            if User.objects.filter(social_auth__uid= like["id"]).exists() :           
                user = UserSocialAuth.get_social_auth("facebook",like["id"]).user 
                if user not in P.liked_by.all() :
                   P.liked_by.add(user)
                  #give parent_post like points 10 maybe
        if "message_tags" in post.keys() :
          for tag in post["message_tags"] :
            tag,tag_create = Tag.objects.get_or_create(tag_id= tag["id"] ,tag= tag["name"] )
            if tag not in P.tags.all() :
                P.tags.add(tag) 
        P.save()



def get_user_posts() :
    api = facebook.GraphAPI(access_token=app_token ,version="2.12")
    for user in User.objects.filter(ca_details__ca_approval =True,ca_details__ca_profile_complete=True) :
            user_posts = api.get_connections(id=user.social_auth.get(provider="facebook").uid ,connection_name="feed",fields="id,parent_id,created_time,reactions,shares,message_tags")
            post_all =[]
            for post in user_posts["data"] :
                if PagePost.objects.filter(post_id = post["parent_id"]).exists() :

                    print(post)
                    shared_post = PagePost.objects.get(post_id = post["parent_id"]) 
                       
                    fbshare,created = UserSharedPost.objects.get_or_create(user = user ,post_id = post["id"] ,shared_post=shared_post)
                    fbshare.shares_cnt = post["shares"]["count"] if "shares" in post.keys() else 0
                    fbshare.likes_cnt = len(post["reactions"]["data"]) if "reactions" in post.keys() else 0
                    

                    if "message_tags" in post.keys() :
                        for tag in post["message_tags"] :
                            if Tag.objects.filter(tag_id = tag["id"]).exists() :
                                fbshare.tags.add(Tag.objects.get(tag_id = tag["id"]))

                    
                    if created :
                        fbshare.created_at = post["created_time"]
                        print("created")
                        #give post share poins 

                    else :

                        print("hello")
                        #revaluate tag,likes ,shares of shared post points 
                    
                    fbshare.save()
                    post_all.append(fbshare.pk)




            posts_q = UserSharedPost.objects.filter(user = user).exclude(pk__in=post_all).all()
            for p in posts_q :
                p.delete()






             

        


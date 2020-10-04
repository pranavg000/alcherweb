from django.contrib import admin
from .models import Tag, PagePost, UserSharedPost,InviteAll
from ca.scores import FB_SHARE_SCORE

class UserSharedPostAdmin(admin.ModelAdmin):
    readonly_fields = ['likes_score','tags_score','shares_score','post_share_score']
    ''' def save_model(self,request,obj,form,change):
        if 'admin_approval' in form.changed_data:
            delta = -FB_SHARE_SCORE
            if obj.pk:
                approval = obj.admin_approval
                if not approval:
                    pass
                else:
                    delta = 0
                obj.post_share_score+=delta
                obj.user.ca_details.score+=delta
                obj.user.ca_details.fbscore+=delta

                super().save_model(request, obj, form, change)
                obj.user.ca_details.save()   '''



class InviteAdmin(admin.ModelAdmin):
        readonly_fields = ['invitesScore','triweekly_invite']
        def save_model(self, request, obj, form, change):
                if 'approval' in form.changed_data:
  
                        delta = FB_SHARE_SCORE
                        if obj.pk:
                                old_value = InviteAll.objects.get(pk=obj.pk).approval
                                if old_value == 1:
                                        delta = -FB_SHARE_SCORE
                                elif (old_value == -1 and obj.approval == 0) or (old_value == 0 and obj.approval == -1):
                                        delta = 0

  
                        elif obj.approval != 1:
                                delta = 0                       

                        obj.invitesScore+=delta
                        obj.user.ca_details.fbscore+=delta
                        obj.user.ca_details.score+=delta
                        if  delta > 0 or obj.triweekly_invite!= 0 :
                            obj.triweekly_invite+=delta
                            obj.user.ca_details.triweekly+=delta

                super().save_model(request, obj, form, change)
                obj.user.ca_details.save()
        
        def delete_model(self,request,obj):
                if obj.invitesScore == FB_SHARE_SCORE:
                        obj.user.ca_details.score-=FB_SHARE_SCORE
                        obj.user.ca_details.fbscore -=FB_SHARE_SCORE
                if obj.triweekly_invite == FB_SHARE_SCORE:
                           obj.user.ca_details.triweekly-=FB_SHARE_SCORE
                
                super().delete_model(request,obj)
                obj.user.ca_details.save()




"""class UserManualSharedPostAdmin(admin.ModelAdmin):
    readonly_fields = ['post_share_score']
    def save_model(self,request,obj,form,change):
        if 'admin_approval' in form.changed_data:
            delta = FB_SHARE_SCORE
            approval = obj.admin_approval
            if obj.pk:
                if not approval:
                    delta = -FB_SHARE_SCORE
            else:
                if not approval:
                    delta = 0
        else:
            delta = 0

        obj.post_share_score+=delta
        obj.user.ca_details.fbscore+=delta
        obj.user.ca_details.score+=delta
        super().save_model(request, obj, form, change)
        obj.user.ca_details.save()"""






admin.site.register(Tag)
admin.site.register(PagePost)

admin.site.register(InviteAll,InviteAdmin)

#admin.site.register(UserManualSharedPost, UserManualSharedPostAdmin)
# Register your models here
admin.site.register(UserSharedPost,UserSharedPostAdmin)

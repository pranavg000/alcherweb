from django.contrib import admin
from .models import *




class InviteAdmin(admin.ModelAdmin):
        readonly_fields = ['invitesScore','triweekly_invite']
        def save_model(self, request, obj, form, change):
                if 'approval' in form.changed_data:
  
                        delta = 50
                        if obj.pk:
                                old_value = InviteAll.objects.get(pk=obj.pk).approval
                                if old_value == 1:
                                        delta = -50
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
                if obj.invitesScore == 50:
                        obj.user.ca_details.score-=50
                        obj.user.ca_details.fbscore -=50
                if obj.triweekly_invite == 50:
                           obj.user.ca_details.triweekly-=50
                
                super().delete_model(request,obj)
                obj.user.ca_details.save()










admin.site.register(Tag)
admin.site.register(PagePost)
admin.site.register(UserSharedPost)
admin.site.register(InviteAll,InviteAdmin)


# Register your models here.

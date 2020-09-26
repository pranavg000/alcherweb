from django.contrib import admin
from .models import *


class UserSharedPostAdmin(admin.ModelAdmin):
    readonly_fields = ['likes_score','tags_score','shares_score','post_share_score','parent_post_like_score']
    def save_model(self,request,obj,form,change):
        if 'admin_approval' in form.changed_data:
            delta = -30
            if obj.pk:
                approval = obj.admin_approval
                if not approval:
                    pass
                else:
                    delta = 0
        obj.post_share_score+=delta
        obj.user.ca_details.score+=delta
        super().save_model(request, obj, form, change)
        obj.user.ca_details.save()


admin.site.register(Tag)
admin.site.register(PagePost)
admin.site.register(UserSharedPost,UserSharedPostAdmin)

import decimal, csv
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F
from .models import CA_Detail, Profile, Interest
from ca.models import Idea,Venue,POC
from ca.scores import REFERRAL_SCORE


def ca_approve(modeladmin, request, queryset):	
		for ca in queryset:
			if ca.ca_approval==False:
				ca.score += 50
				ca.ca_approval=True
			ca.save()
ca_approve.short_description = 'Approve all the selected CAs'

def ca_disapprove(modeladmin, request, queryset):	
		for ca in queryset:
			if ca.ca_approval==True:
				ca.score-=50
				ca.ca_approval=False
			ca.save()
ca_disapprove.short_description = 'Disapprove all the selected CAs'

def certificate_approve(modeladmin, request, queryset):
		for ca in queryset:
			ca.certificate_approval=True
			ca.save()
certificate_approve.short_description = 'Approve certificate for all the selected CAs'
		
def certificate_disapprove(modeladmin, request, queryset):
		for ca in queryset:
			ca.certificate_approval=False
			ca.save()
certificate_disapprove.short_description = 'Disapprove certificate for all the selected CAs'

def export_CA(modeladmin, request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="ca.csv"'
	writer = csv.writer(response)
	writer.writerow(['Username', 'CA Approval', 'Certificate Approval', 'Score', 'FBscore'])
	cas = queryset.values_list('user', 'ca_approval', 'certificate_approval', 'score', 'fbscore')
	for ca in cas:
		writer.writerow(ca)
	return response
export_CA.short_description = 'Export CA data to csv'


class CAadmin(admin.ModelAdmin):
#	readonly_fields=['score','triweekly','fbscore']
	# change_list_template = "auths/CAadmin.html"

	#Code for resetting TriWeekly Event Score
	# def get_urls(self):
	# 	urls = super().get_urls()
	# 	my_urls = [path('resetscore/', self.resetscore),]
	# 	return my_urls + urls

	# def resetscore(self, request):
	# 	self.model.objects.all().update(triweekly=0)
	# 	Idea.objects.all().update(triweeklyidea=0)
	# 	POC.objects.all().update(triweeklyPOC=0)
	# 	Venue.objects.all().update(triweeklyvenue=0)
	# 	self.message_user(request, "triweekly scores have been reset")
	# 	return HttpResponseRedirect("../")

	list_display = ('user', 'score', 'fbscore', 'ca_profile_complete', 'ca_approval', 'certificate_approval')
	list_filter = ("ca_profile_complete", "ca_approval", "certificate_approval",)
	search_fields = ['user']
	actions = [ca_approve, ca_disapprove, certificate_approve, certificate_disapprove, export_CA, ]

	def save_model(self, request, obj, form, change):
		if 'ca_approval' in form.changed_data:
			ref_code = ""
			delta = -REFERRAL_SCORE
			if obj.pk:
				ref_code = obj.user.ca_questionnaire.referral_code
				if obj.ca_approval:
					delta *= -1
				

			if ref_code:
				try:
					referrer_ca_details = Profile.objects.get(alcher_id=ref_code).user.ca_details
					referrer_ca_details.score += delta
					referrer_ca_details.save()
				except:
					pass
		super().save_model(request, obj, form, change)




class ProfileAdmin(admin.ModelAdmin):	
	list_display = ('alcher_id', 'user', 'fullname', 'college', 'phone',)
	search_fields =['alcher_id', 'phone', 'state', 'interests',]
	list_filter = ("interests",)


admin.site.register(Interest)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CA_Detail, CAadmin)

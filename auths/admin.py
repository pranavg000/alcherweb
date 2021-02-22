import decimal, csv
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F
from .models import CA_Detail, Profile
from ca.models import Idea,Venue,POC, CA_Questionnaire
from ca.scores import REFERRAL_SCORE
from django.contrib.auth.models import User

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
	writer.writerow(['Username', 'CA Approval', 'Certificate Approval', 'Score', 'FBscore',])
	cas = queryset.values_list('user_id', 'ca_approval', 'certificate_approval', 'score', 'fbscore',)
	for ca in cas:
		writer.writerow(ca)
	return response
export_CA.short_description = 'Export CA data to csv'

# class CAInline(admin.StackedInline):
#['ALC ID', 'User', 'Full Name', 'College', 'Phone', 'City', 'Mailing Address', 'Alt. Contact', 'Email ID', 'CA Approval', 'Certificate Approval']

class CAadmin(admin.ModelAdmin):
	list_display = ('user', 'score', 'fbscore', 'ca_profile_complete', 'ca_approval', 'certificate_approval')
	list_filter = ("ca_profile_complete", "ca_approval", "certificate_approval",)
	search_fields = ['user']
	actions = [ca_approve, ca_disapprove, certificate_approve, certificate_disapprove, export_CA, ]
	# inlines = [CAInline]

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
	search_fields =['alcher_id', 'phone', 'state',]
	actions = ["export_profiles", ]

	def export_profiles(self, request, queryset):	
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="caprofile.csv"'
		writer = csv.writer(response)
		writer.writerow(['Username' ,'Alcher ID', 'Full Name', 'Phone', 'College'])
		caprofiles = queryset.values_list('user', 'alcher_id', 'fullname', 'phone', 'college')
		for profile in caprofiles:
			writer.writerow(profile)
		
		self.message_user(request, "All the profiles have been exported successfully.")
		return response
	export_profiles.short_description = 'Export CA profiles to CSV'
	

# admin.site.register(Interest)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CA_Detail, CAadmin)

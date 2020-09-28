from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from .models import *
from ca.models import Idea,Venue,POC


class CAadmin(admin.ModelAdmin):
	readonly_fields=['score','triweekly','fbscore']
	change_list_template = "auths/CAadmin.html"

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [path('resetscore/', self.resetscore),]
		return my_urls + urls

	def resetscore(self, request):
		self.model.objects.all().update(triweekly=0)
		Idea.objects.all().update(triweeklyidea=0)
		POC.objects.all().update(triweeklyPOC=0)
		Venue.objects.all().update(triweeklyvenue=0)
		self.message_user(request, "triweekly scores have been reset")
		return HttpResponseRedirect("../")

	def save_model(self, request, obj, form, change):
		if 'ca_approval' in form.changed_data:
			ref_code = ""
			delta = -50
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


	


admin.site.register(Interest)
admin.site.register(Profile)
admin.site.register(CA_Detail, CAadmin)

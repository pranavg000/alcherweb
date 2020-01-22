from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from .models import *
from ca.models import Idea,Venue,POC


class CAadmin(admin.ModelAdmin):
	readonly_fields=['score','triweekly']
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

admin.site.register(Interest)
admin.site.register(Profile)
admin.site.register(CA_Detail, CAadmin)

from django.contrib import admin
from .models import *
from auths.models import *


class IdeaAdmin(admin.ModelAdmin):
	readonly_fields = ['ideascore','triweeklyidea',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:
			if obj.approval == 1:
				obj.ideascore+=50
				obj.triweeklyidea+=50
				obj.user.ca_details.score+=50
				obj.user.ca_details.triweekly+=50
			if obj.approval == 0:
				obj.ideascore-=50
				obj.user.ca_details.score-=50
				if obj.triweeklyidea!=0:
					obj.triweeklyidea-=50
					obj.user.ca_details.triweekly-=50
		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.ideascore!=0:
			obj.user.ca_details.score-=50
		if obj.triweeklyidea!=0:
			obj.user.ca_details.triweekly-=50
		super().delete_model(request,obj)
		obj.user.ca_details.save()


class POCAdmin(admin.ModelAdmin):
	readonly_fields = ['POCscore','triweeklyPOC',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:
			if obj.approval == 1:
				obj.POCscore+=50
				obj.triweeklyPOC+=50
				obj.user.ca_details.score+=50
				obj.user.ca_details.triweekly+=50
			if obj.approval == 0:
				obj.POCscore-=50
				obj.user.ca_details.score-=50
				if obj.triweeklyPOC!=0:
					obj.triweeklyPOC-=50
					obj.user.ca_details.triweekly-=50
		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.POCscore!=0:
			obj.user.ca_details.score-=50
		if obj.triweeklyPOC!=0:
			obj.user.ca_details.triweekly-=50
		super().delete_model(request,obj)
		obj.user.ca_details.save()

class VenueAdmin(admin.ModelAdmin):
	readonly_fields = ['venuescore','triweeklyvenue',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:
			if obj.approval == 1:
				obj.venuescore+=300
				obj.triweeklyvenue+=300
				obj.user.ca_details.score+=300
				obj.user.ca_details.triweekly+=300
			if obj.approval == 0:
				obj.venuescore-=300
				obj.user.ca_details.score-=300
				if obj.triweeklyvenue!=0:
					obj.triweeklyvenue-=300
					obj.user.ca_details.triweekly-=300
		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.venuescore!=0:
			obj.user.ca_details.score-=300
		if obj.triweeklyvenue!=0:
			obj.user.ca_details.triweekly-=300
		super().delete_model(request,obj)
		obj.user.ca_details.save()



admin.site.register(Complaints)
admin.site.register(FAQ)
admin.site.register(Idea,IdeaAdmin)
admin.site.register(POC,POCAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(CA_Questionnaire)
admin.site.register(TriweekyWinner)



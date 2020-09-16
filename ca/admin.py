from django.contrib import admin
from .models import *
from auths.models import *


class IdeaAdmin(admin.ModelAdmin):
	readonly_fields = ['ideascore','triweeklyidea',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:
			if obj.pk:
				old_value = Idea.objects.get(pk=obj.pk).approval
				delta = 50
				if old_value == 1:
					delta = -50
				elif (old_value == -1 and obj.approval == 0) or (old_value == 0 and obj.approval == -1):
					delta = 0

				
			else:
				if obj.approval == 1:
					delta = 50
				else:
					delta = -50

			obj.ideascore+=delta
			obj.user.ca_details.score+=delta
			if  delta > 0 or obj.triweeklyidea!=0:
				obj.triweeklyidea+=delta
				obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.ideascore == 50:
			obj.user.ca_details.score-=50
		if obj.triweeklyidea == 50:
			obj.user.ca_details.triweekly-=50
		super().delete_model(request,obj)
		obj.user.ca_details.save()


class POCAdmin(admin.ModelAdmin):
	readonly_fields = ['POCscore','triweeklyPOC',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:
			if obj.pk:
				old_value = POC.objects.get(pk=obj.pk).approval
				delta = 50
				if old_value == 1:
					delta = -50
				elif (old_value == -1 and obj.approval == 0) or (old_value == 0 and obj.approval == -1):
					delta = 0

				
			else:
				if obj.approval == 1:
					delta = 50
				else:
					delta = -50

			obj.POCscore+=delta
			obj.user.ca_details.score+=delta
			if  delta > 0 or obj.triweeklyPOC!=0:
				obj.triweeklyPOC+=delta
				obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.POCscore == 50:
			obj.user.ca_details.score-=50
		if obj.triweeklyPOC == 50:
			obj.user.ca_details.triweekly-=50
		super().delete_model(request,obj)
		obj.user.ca_details.save()

class VenueAdmin(admin.ModelAdmin):
	readonly_fields = ['venuescore','triweeklyvenue',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:

			if obj.pk:
				old_value = Venue.objects.get(pk=obj.pk).approval
				delta = 300
				if old_value == 1:
					delta = -300
				elif (old_value == -1 and obj.approval == 0) or (old_value == 0 and obj.approval == -1):
					delta = 0

				
			else:
				if obj.approval == 1:
					delta = 300
				else:
					delta = -300

			obj.venuescore+=delta
			obj.user.ca_details.score+=delta
			if  delta > 0 or obj.triweeklyvenue!=0:
				obj.triweeklyvenue+=delta
				obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.venuescore == 300:
			obj.user.ca_details.score-=300
		if obj.triweeklyvenue == 300:
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
admin.site.register(Notifications)



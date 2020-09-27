from django.contrib import admin
from .models import *
from auths.models import *
from ca.scores import IDEA_SCORE, POC_SCORE, VENUE_SCORE

class IdeaAdmin(admin.ModelAdmin):
	readonly_fields = ['ideascore','triweeklyidea',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:
			delta = IDEA_SCORE
			if obj.pk:
				old_value = Idea.objects.get(pk=obj.pk).approval
				if old_value == 1:
					delta = -IDEA_SCORE
				elif (old_value == -1 and obj.approval == 0) or (old_value == 0 and obj.approval == -1):
					delta = 0
			
			elif obj.approval != 1:
				delta = 0


			obj.ideascore+=delta
			obj.user.ca_details.score+=delta
			if  delta > 0 or obj.triweeklyidea!=0:
				obj.triweeklyidea+=delta
				obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.ideascore == IDEA_SCORE:
			obj.user.ca_details.score-=IDEA_SCORE
		if obj.triweeklyidea == IDEA_SCORE:
			obj.user.ca_details.triweekly-=IDEA_SCORE
		super().delete_model(request,obj)
		obj.user.ca_details.save()


class POCAdmin(admin.ModelAdmin):
	readonly_fields = ['POCscore','triweeklyPOC',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:
			delta = POC_SCORE
			if obj.pk:
				old_value = POC.objects.get(pk=obj.pk).approval
				if old_value == 1:
					delta = -POC_SCORE
				elif (old_value == -1 and obj.approval == 0) or (old_value == 0 and obj.approval == -1):
					delta = 0

				
			elif obj.approval != 1:
				delta = 0

			obj.POCscore+=delta
			obj.user.ca_details.score+=delta
			if  delta > 0 or obj.triweeklyPOC!=0:
				obj.triweeklyPOC+=delta
				obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.POCscore == POC_SCORE:
			obj.user.ca_details.score-=POC_SCORE
		if obj.triweeklyPOC == POC_SCORE:
			obj.user.ca_details.triweekly-=POC_SCORE
		super().delete_model(request,obj)
		obj.user.ca_details.save()

class VenueAdmin(admin.ModelAdmin):
	readonly_fields = ['venuescore','triweeklyvenue',]
	def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:

			delta = VENUE_SCORE
			if obj.pk:
				old_value = Venue.objects.get(pk=obj.pk).approval
				if old_value == 1:
					delta = -VENUE_SCORE
				elif (old_value == -1 and obj.approval == 0) or (old_value == 0 and obj.approval == -1):
					delta = 0

				
			elif obj.approval != 1:
				delta = 0

			obj.venuescore+=delta
			obj.user.ca_details.score+=delta
			if  delta > 0 or obj.triweeklyvenue!=0:
				obj.triweeklyvenue+=delta
				obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.venuescore == VENUE_SCORE:
			obj.user.ca_details.score-=VENUE_SCORE
		if obj.triweeklyvenue == VENUE_SCORE:
			obj.user.ca_details.triweekly-=VENUE_SCORE
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



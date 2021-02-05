from django.contrib import admin
#from .models import Idea, POC, FAQ, Venue, Complaints, Notifications, TriweekyWinner, CA_Questionnaire
from .models import Idea, POC, FAQ, Venue, Complaints, Notifications, CA_Questionnaire
from auths.models import CA_Detail
from ca.scores import IDEA_SCORE, POC_SCORE, VENUE_SCORE
from django.http import HttpResponse
import csv

class IdeaAdmin(admin.ModelAdmin):
	list_display = ('user', 'idea_category', 'idea', 'admin_reply', 'approval', 'ideascore' )
	list_filter = ("idea_category", "approval",)
	search_fields = ['user']
	readonly_fields = ['ideascore']
	#Use this when including triweeklyidea
	# readonly_fields = ['ideascore','triweeklyidea',]
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
			# if  delta > 0 or obj.triweeklyidea!=0:
			# 	obj.triweeklyidea+=delta
			# 	obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.ideascore == IDEA_SCORE:
			obj.user.ca_details.score-=IDEA_SCORE
		# if obj.triweeklyidea == IDEA_SCORE:
		# 	obj.user.ca_details.triweekly-=IDEA_SCORE
		super().delete_model(request,obj)
		obj.user.ca_details.save()


class POCAdmin(admin.ModelAdmin):
	# readonly_fields = ['POCscore','triweeklyPOC',]
	list_display = ('user', 'genre', 'name_con', 'desg', 'colg', 'phone', 'fburl', 'email', 'approval')
	list_filter = ("genre", "approval",)
	readonly_fields = ['POCscore',]
	actions = ["approve_poc", "disapprove_poc",]

	def approve_poc(self, request, queryset):
		for venue in queryset:
			venue.approval=True
			venue.save()
		
		self.message_user(request, "All the selected PoCs have been approved successfully.")
	approve_poc.short_description = 'Approve all the selected PoCs'

	def disapprove_poc(self, request, queryset):
		for venue in queryset:
			venue.approval=False
			venue.save()
		self.message_user(request, "All the selected PoCs have been disapproved successfully.")
	disapprove_poc.short_description = 'Disapprove all the selected PoCs'

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
			#TriWeekly score function
			# if  delta > 0 or obj.triweeklyPOC!=0:
			# 	obj.triweeklyPOC+=delta
			# 	obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.POCscore == POC_SCORE:
			obj.user.ca_details.score-=POC_SCORE

		#TriWeekly function
		# if obj.triweeklyPOC == POC_SCORE:
		# 	obj.user.ca_details.triweekly-=POC_SCORE
		super().delete_model(request,obj)
		obj.user.ca_details.save()

class VenueAdmin(admin.ModelAdmin):
	# readonly_fields = ['venuescore','triweeklyvenue',]

	list_display = ('user', 'venue_name', 'venue_address', 'contact_name', 'contact_number', 'remarks', 'approval')
	list_filter = ("approval", )
	readonly_fields = ['venuescore',]
	actions = ["approve_venue", "disapprove_venue",]

	def approve_venue(self, request, queryset):
		for venue in queryset:
			venue.approval=True
			venue.save()
		
		self.message_user(request, "All the selected venues have been approved successfully.")
	approve_venue.short_description = 'Approve all the selected Venues'

	def disapprove_venue(self, request, queryset):
		for venue in queryset:
			venue.approval=False
			venue.save()
		self.message_user(request, "All the selected venues have been disapproved successfully.")
	disapprove_venue.short_description = 'Disapprove all the selected Venues'

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
			#TriWeekly score function
			# if  delta > 0 or obj.triweeklyvenue!=0:
			# 	obj.triweeklyvenue+=delta
			# 	obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.venuescore == VENUE_SCORE:
			obj.user.ca_details.score-=VENUE_SCORE
		# if obj.triweeklyvenue == VENUE_SCORE:
		# 	obj.user.ca_details.triweekly-=VENUE_SCORE
		super().delete_model(request,obj)
		obj.user.ca_details.save()


class FAQAdmin(admin.ModelAdmin):
	list_display = ('faq_question', 'faq_category')
	list_filter = ("faq_category", )

class NotificationsAdmin(admin.ModelAdmin):
	list_display = ('notification_sender', 'notification_receiver', 'notification_content', 'notification_href', 'notification_timestamp')
	list_filter = ("notification_timestamp", )

class CA_QuestionnaireAdmin(admin.ModelAdmin):
	list_display = ('user', 'college_name', 'city', 'alt_contact', 'mailing_address', 'state', 'city', 'full_name')
	list_filter = ("state", "city", )
	search_fields = ['state', 'city']
	actions = ["export_csv"]

	def export_csv(self, request, queryset):
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="ca_profile.csv"'
		writer = csv.writer(response)
		writer.writerow(['Full Name', 'State', 'City', 'Alt_Contact', 'Username', 'Mailing Address'])
		ca_profiles = queryset.values_list('full_name', 'state', 'city', 'alt_contact', 'user', 'mailing_address')
		for ca_profile in ca_profiles:
			writer.writerow(ca_profile)
		return response
	export_csv.short_description = 'Export data to csv'

class ComplaintsAdmin(admin.ModelAdmin):
	list_display = ('grievance_id', 'complaint_category', 'user', 'complaint_stat', 'complaint_text', 'complaint_report')
	list_filter = ("complaint_stat", "complaint_category",)
	search_fields = ['grievance_id', 'user']

admin.site.register(Complaints, ComplaintsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Idea,IdeaAdmin)
admin.site.register(POC,POCAdmin)
# admin.site.register(Venue, VenueAdmin)
admin.site.register(CA_Questionnaire,CA_QuestionnaireAdmin)
# admin.site.register(TriweekyWinner)
admin.site.register(Notifications, NotificationsAdmin)



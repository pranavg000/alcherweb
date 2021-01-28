from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
from .choices import *
from auths.models import Profile
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from ca.scores import REFERRAL_SCORE


class Complaints(models.Model):
	# complaint_id = models.IntegerField(default=0,validators=[MinValueValidator(0)])
	grievance_id = models.CharField(max_length=15)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	complaint_category = models.CharField(choices=COMPLAINT_CATEGORY_CHOICES,default='general',max_length=15)
	complaint_text = models.CharField(max_length=500)
	complaint_stat = models.BooleanField(default=False)
	complaint_report = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.grievance_id


class FAQ(models.Model):
	faq_category = models.CharField(choices=FAQ_CATEGORY_CHOICES,default='general',max_length=15)
	faq_question = models.CharField(max_length=500)
	faq_answer = models.TextField()

	def __str__(self):
		return self.faq_question


class Notifications(models.Model):
	notification_sender = models.CharField(max_length=200, default="Alcheringa Team")
	notification_receiver = models.ForeignKey(User, on_delete=models.CASCADE)
	# notification_receiver = models.CharField(max_length=200)
	notification_content = models.CharField(max_length=500, null=True, blank=True)
	notification_href = models.URLField(max_length=200, null=True, blank=True)
	notification_timestamp = models.DateTimeField(auto_now_add=True)


class Idea(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	idea_category = models.CharField(choices=IDEA_CATEGORY_CHOICES,default='Other',max_length=20)
	idea = models.CharField(max_length=200)
	admin_reply = models.CharField(max_length=200, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	approval = models.BooleanField(default=False)
	ideascore = models.IntegerField(default=0)
	# triweeklyidea = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.user.username} - {self.idea_category}'


class POC(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	genre = models.CharField(choices=GENRE_CHOICES,default='dance',max_length=30)
	name_con = models.CharField(max_length=60)
	desg = models.CharField(max_length=50)
	colg = models.CharField(max_length=100)
	phone = models.CharField(max_length=13)
	fburl = models.URLField(max_length=200)
	email = models.EmailField(max_length=254)
	timestamp = models.DateTimeField(auto_now_add=True)
	approval = models.BooleanField(default=False)
	POCscore = models.IntegerField(default=0)
	# triweeklyPOC = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.user.username} - {self.name_con}'


class Venue(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	venue_name = models.CharField(max_length=200)
	venue_address = models.CharField(max_length=500)
	contact_name = models.CharField(max_length=100)
	contact_number = models.CharField(max_length=10)
	remarks = models.CharField(max_length=500, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	approval = models.BooleanField(default=False)
	venuescore = models.IntegerField(default=0)
	# triweeklyvenue = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.user.username} - {self.venue_name}'



class CA_Questionnaire(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ca_questionnaire')
	alt_contact = models.CharField(max_length=13)
	college_name = models.CharField(max_length=200)
	state = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=200)
	mailing_address = models.CharField(max_length=500)
	fb = models.URLField(max_length=200)
	por = models.CharField(max_length=500)
	referral_code = models.CharField(max_length=200,blank=True)



# class TriweekyWinner(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE) 



@receiver(pre_delete, sender=CA_Questionnaire, dispatch_uid='questionnare_delete_signal')
def update_referrer_score(sender, instance, using, **kwargs):
	ref_code = instance.referral_code
	if ref_code and instance.user.ca_details.ca_approval:
		try:
			referrer_ca_details = Profile.objects.get(alcher_id=ref_code).user.ca_details
			referrer_ca_details.score -= REFERRAL_SCORE
			referrer_ca_details.save()
		except:
			pass

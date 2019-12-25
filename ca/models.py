from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User


class Complaints(models.Model):

	COMPLAINT_CATEGORY_CHOICES = {
	('general', 'General'),
	('technical', 'Technical'),
	('competition', 'Competition'),
	('festival', 'Festival'),
	('payment', 'Payment'),
	}

	# complaint_id = models.IntegerField(default=0,validators=[MinValueValidator(0)])
	grievance_id = models.CharField(max_length=15)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	complaint_category = models.CharField(choices=COMPLAINT_CATEGORY_CHOICES,default='general',max_length=15)
	complaint_text = models.CharField(max_length=500)
	complaint_stat = models.BooleanField(default=False)
	complaint_report = models.CharField(max_length=500, null=True)


class FAQ(models.Model):
	FAQ_CATEGORY_CHOICES = {
	('general', 'GENERAL'),
	('portal', 'PORTAL'),
	('competition', 'COMPETITIONS'),
	('accommodation', 'ACCOMMODATION'),
	('audition', 'CITY AUDITION'),
	}

	faq_category = models.CharField(choices=FAQ_CATEGORY_CHOICES,default='general',max_length=15)
	faq_question = models.CharField(max_length=500)
	faq_answer = models.CharField(max_length=500)


class Notifications(models.Model):
	notification_sender = models.CharField(max_length=200)
	notification_receiver = models.ForeignKey(User, on_delete=models.CASCADE)
	# notification_receiver = models.CharField(max_length=200)
	notification_content = models.CharField(max_length=500, null=True, blank=True)
	notification_href = models.URLField(max_length=200, null=True, blank=True)
	notification_timestamp = models.DateTimeField(auto_now_add=True)


class Idea(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	idea = models.CharField(max_length=200)
	admin_reply = models.CharField(max_length=200, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	approval = models.IntegerField(default=0)


class POC(models.Model):
	GENRE_CHOICES = {
	('dance','Dance'),
	('music','Music'),
	('drama','Drama'),
	('arts','Arts'),
	('fashion','Fashion'),
	('lit_n_deb','Literary and Debate'),
	('sports','Sports'),	
	}

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	genre = models.CharField(choices=GENRE_CHOICES,default='dance',max_length=20)
	name_con = models.CharField(max_length=60)
	desg = models.CharField(max_length=50)
	colg = models.CharField(max_length=100)
	phone = models.CharField(max_length=13)
	fb = models.URLField(max_length=200)
	email = models.EmailField(max_length=254)
	timestamp = models.DateTimeField(auto_now_add=True)
	approval = models.IntegerField(default=0)


class Venue(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	venue_name = models.CharField(max_length=200)
	venue_add = models.CharField(max_length=500)
	contact_name = models.CharField(max_length=100)
	contact_no = models.CharField(max_length=13)
	remarks = models.CharField(max_length=500, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	approval = models.IntegerField(default=0)



class CA_Questionnaire(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	alt_contact = models.CharField(max_length=13)
	acad = models.CharField(max_length=100)
	college_name = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	mailing_address = models.CharField(max_length=500)
	fb = models.URLField(max_length=200)
	por = models.CharField(max_length=500)
	referral_code = models.CharField(max_length=200)
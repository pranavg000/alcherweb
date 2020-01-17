from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User


class Complaints(models.Model):

	COMPLAINT_CATEGORY_CHOICES = {
		('General', 'General'),
		('Technical', 'Technical'),
		('Competition', 'Competition'),
		('Festival', 'Festival'),
		('Payment', 'Payment'),
		}

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
	IDEA_CATEGORY_CHOICES = {
	('Competition', 'Competition'),
	('Workshop', 'Workshop'),
	('Hospitality', 'Hospitality'),
	('Artist', 'Artist'),
	('Crowd Experience', 'Crowd Experience'),
	('Other', 'Other'),
	}
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	idea_category = models.CharField(choices=IDEA_CATEGORY_CHOICES,default='Other',max_length=20)
	idea = models.CharField(max_length=200)
	admin_reply = models.CharField(max_length=200, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	approval = models.IntegerField(default=0)


class POC(models.Model):
	GENRE_CHOICES = {
	('Dance','Dance'),
	('Music','Music'),
	('Drama','Drama'),
	('Arts','Arts'),
	('Fashion','Fashion'),
	('Literary and Debate','Literary and Debate'),
	('Sports','Sports'),	
	}

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	genre = models.CharField(choices=GENRE_CHOICES,default='dance',max_length=30)
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
	venue_address = models.CharField(max_length=500)
	contact_name = models.CharField(max_length=100)
	contact_number = models.CharField(max_length=13)
	remarks = models.CharField(max_length=500, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	approval = models.IntegerField(default=0)

	def __str__(self):
		return self.venue_name



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
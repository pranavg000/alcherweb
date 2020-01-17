from django.shortcuts import render, redirect
from ca.models import * 
from auths.models import CA_Detail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from random import randint
from django.core.validators import RegexValidator, EmailValidator


def generateGrievanceId():
	try:
		lpk = Complaints.objects.last().pk+1
	except Exception as e:
		lpk = 1
	return "CX"+str(randint(1563,9874))+str(lpk)



@login_required
def contactUs(request):
	if request.method == 'POST':
		COMPLAINT_CATEGORY_CHOICES = {
		('General', 'General'),
		('Technical', 'Technical'),
		('Competition', 'Competition'),
		('Festival', 'Festival'),
		('Payment', 'Payment'),
		}
		complaint_category_list = [x[0] for x in COMPLAINT_CATEGORY_CHOICES]
		data = {}
		if request.POST['complaint_category'] == '':
			 data['complaint_category_stat'] = "Complaint category empty"
		if request.POST['complaint_category'] not in complaint_category_list:
			 data['complaint_category_stat'] = "INVALID COMPLAINT CATEGORY"

		if request.POST['complaint_text'] == '':
			 data['complaint_text_stat'] = "Complaint text empty"

		if data.get('category') or data.get('desc'):
			data['stat'] = "FAILURE"
			return JsonResponse(data)
		else :
			complaint_text = request.POST['complaint_text']
			complaint_category = request.POST['complaint_category']
			grievance_id = generateGrievanceId()

			Complaints.objects.create(user=request.user, complaint_text=complaint_text, 
				complaint_category=complaint_category, grievance_id=grievance_id)
			data['grievance_id']= grievance_id
			data['stat'] = "SUCCESS"

		return JsonResponse(data)
	else:
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:pending')
		elif not ca_dets.ca_profile_complete :
			return redirect('ca:questionnare')
		else :
			prevQueries = Complaints.objects.filter(user=request.user).order_by('-pk')

			context = {
			'prevQueries': prevQueries,
			'more_active': True,
			}

			return render(request, 'ca/contacts.html', context)


@login_required
def submitIdea(request):
	if request.method == 'POST':
		IDEA_CATEGORY_CHOICES = {
		('Competition', 'Competition'),
		('Workshop', 'Workshop'),
		('Hospitality', 'Hospitality'),
		('Artist', 'Artist'),
		('Crowd Experience', 'Crowd Experience'),
		('Other', 'Other'),
		}
		idea_category_list = [x[0] for x in IDEA_CATEGORY_CHOICES]
		data = {}
		if request.POST['idea_category'] == '' or request.POST['idea_category'] not in idea_category_list:
			 data['category'] = "Category Empty"

		if request.POST['idea_desc'] == '':
			 data['desc'] = "Desc Empty"

		if data.get('category') or data.get('desc'):
			data['stat'] = "Failure"
			return JsonResponse(data)
		else :
			idea = request.POST['idea_desc']
			idea_category = request.POST['idea_category']
			Idea.objects.create(user=request.user, idea=idea, idea_category=idea_category)
			data['stat'] = "Success"

		return JsonResponse(data)
	else:
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:pending')
		elif not ca_dets.ca_profile_complete :
			return redirect('ca:questionnare')
		else :
			ideaQueries = Idea.objects.filter(user=request.user).order_by('-pk')

			context = {
				'ideaQueries': ideaQueries,
				'idea_active': True,
			}

			return render(request, 'ca/idea.html', context)

@login_required
def faqs(request):
	if request.method == 'POST':
		faq_category = request.POST['faq_category']
		faqs = FAQ.objects.filter(faq_category=faq_category)

		context = {
		'faqs':faqs,
		}

		return render(request, 'ca/faq_response.html', context)

	else:
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:pending')
		elif not ca_dets.ca_profile_complete :
			return redirect('ca:questionnare')
		else :
			return render(request, 'ca/faq.html', {'more_active': True})


@login_required
def venue(request):
	if request.method == 'POST':
		
		data = {}
		if request.POST['venue_name'] == '':
			data['venue_name'] = "Venue Name Empty"
		
		if request.POST['contact_person'] == '':
			data['contact_person'] = "Contact Person Empty"

		if request.POST['contact_number'] == '':
			data['contact_number'] = "Contact Number Empty"

		if request.POST['venue_address'] == '':
					 data['venue_address'] = "Venue Address Empty"

		contact_number_validator = RegexValidator('^[0-9]{10}$')
		try:
			contact_number_validator(request.POST['contact_number'])
		except Exception as e:
			data['contact_number'] = "Contact Number REGEX"

		if data.get('venue_name') or data.get('contact_person') or data.get('contact_number') or data.get('venue_address') or data.get('contact_number'):
			data['stat'] = "FAILURE"
			return JsonResponse(data)
		else :
			venue_name = request.POST['venue_name']
			contact_person = request.POST['contact_person']
			contact_number = request.POST['contact_number']
			venue_address = request.POST['venue_address']
			remarks = request.POST['remarks']
			Venue.objects.create(user=request.user, venue_name=venue_name, contact_name=contact_person,
				contact_number=contact_number, venue_address=venue_address, remarks=remarks)
			data['stat'] = "Success"

			return JsonResponse(data)

	else:
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:pending')
		elif not ca_dets.ca_profile_complete :
			return redirect('ca:questionnare')
		else :
			venues = Venue.objects.filter(user=request.user).order_by('-pk')
			name_pattern = "[A-Za-z ]+";
			team_name_pattern = "[A-Za-z0-9, ]+";
			phone_pattern = "[0-9]{10}";

			context = {
			'venues': venues,
			'name_pattern':name_pattern,
			'team_name_pattern':team_name_pattern,
			'phone_pattern':phone_pattern,
			'more_active': True,
			}

			return render(request, 'ca/venue.html', context)



@login_required
def questionnare(request):
	if request.method == 'POST':
		alt_contact = request.POST['alt_contact']
		acad = request.POST['acad']
		college_name = request.POST['college_name']
		city = request.POST['city']
		mailing_address = request.POST['mailing_address']
		fb = request.POST['fb']
		por = request.POST['por']
		referral_code = request.POST['referral']

		print(alt_contact, acad,"$$$$$$$$$$$$$$$$$$$$")

		CA_Questionnaire.objects.create(user = request.user, alt_contact=alt_contact, acad=acad,
			college_name=college_name, city=city, mailing_address=mailing_address, fb=fb, por=por,
			referral_code=referral_code)

		ca_det_user = CA_Detail.objects.get(user=request.user)
		ca_det_user.ca_profile_complete = True
		ca_det_user.save()
		return redirect('ca:pending')
	else :
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and ca_dets.ca_approval :
			return redirect('ca:home')
		elif ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:questionnare')
		else :
			context = {
				'email': request.user.email,
				'phone_no': request.user.profile.phone,
				'college': request.user.profile.college,
			}
			return render(request, 'ca/questionnare.html', context)


@login_required
def home(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/home.html', { 'home_active': True })


@login_required
def guidelines(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/guidelines.html', { 'guidelines_active': True })


@login_required
def pending(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and ca_dets.ca_approval :
		return redirect('ca:home')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/pending.html')


@login_required
def hospitality(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/hospitality.html', {'more_active': True})


@login_required
def poc(request):
	if request.method == 'POST':
		
		data = {}
		if request.POST['poc_genre'] == '':
			data['genre'] = "Genre Empty"
		
		if request.POST['poc_college'] == '':
			data['college'] = "College Empty"

		if request.POST['poc_name'] == '':
			data['poc_name'] = "Name Empty"

		if request.POST['poc_designation'] == '':
					 data['designation'] = "Designation Empty"

		if request.POST['poc_phone'] == '':
					 data['phone'] = "Phone Empty"

		if request.POST['poc_email'] == '':
					 data['email'] = "Email Empty"

		contact_number_validator = RegexValidator('^[0-9]{10}$')
		email_validator = EmailValidator()
		try:
			contact_number_validator(request.POST['poc_phone'])
		except Exception as e:
			data['phone'] = "Phone REGEX"

		try:
			email_validator(request.POST['poc_email'])
		except Exception as e:
			data['email'] = "Email REGEX"

		if data.get('genre') or data.get('college') or data.get('poc_name') or data.get('designation') or data.get('phone') or data.get('email') or data.get('fb'):
			data['stat'] = "FAILURE"
			return JsonResponse(data)
		else :
			poc_genre = request.POST['poc_genre']
			poc_college = request.POST['poc_college']
			poc_name = request.POST['poc_name']
			poc_designation = request.POST['poc_designation']
			poc_phone = request.POST['poc_phone']
			poc_email = request.POST['poc_email']
			poc_fb = request.POST['poc_fb']

			POC.objects.create(user=request.user, genre=poc_genre, colg=poc_college,
				name_con=poc_name, desg=poc_designation, phone=poc_phone, email=poc_email, fb=poc_fb)
			data['stat'] = "Success"

			return JsonResponse(data)
	else:
		ca_dets = request.user.ca_details
		if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
			return redirect('ca:pending')
		elif not ca_dets.ca_profile_complete :
			return redirect('ca:questionnare')
		else :
			return render(request, 'ca/poc.html', {'more_active': True})

@login_required
def standings(request):
	ca_dets = request.user.ca_details
	if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
		return redirect('ca:pending')
	elif not ca_dets.ca_profile_complete :
		return redirect('ca:questionnare')
	else :
		return render(request, 'ca/standings.html', {'more_active': True})
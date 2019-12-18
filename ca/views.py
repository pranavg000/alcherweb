from django.shortcuts import render
from ca.models import * 



def contactUs(request):
	prevQueries = Complaints.objects.filter(user=request.user).order_by('-pk')

	context = {
	'prevQueries': prevQueries,
	}

	return render(request, 'ca/contacts.html', context)


def faqs(request):
	if request.method == 'POST':
		faq_category = request.POST['faq_category']
		faqs = FAQ.objects.filter(faq_category=faq_category)

		context = {
		'faqs':faqs
		}

		return render(request, 'ca/faq_response.html', context)

	else:
		return render(request, 'ca/faq.html')


def venue(request):
	venues = Venue.objects.filter(user=request.user).order_by('-pk')
	name_pattern = "A-Za-z ";
	team_name_pattern = "A-Za-z0-9, ";
	phone_pattern = "0-9";

	context = {
	'venues': venues,
	'name_pattern':name_pattern,
	'team_name_pattern':team_name_pattern,
	'phone_pattern':phone_pattern,
	}

	return render(request, 'ca/venue.html', context)
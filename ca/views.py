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

from django.shortcuts import render, redirect
# from ca.models import Notifications, Idea, Complaints, FAQ, Venue, CA_Questionnaire, POC, TriweekyWinner
from ca.models import Notifications, Idea, Complaints, FAQ, Venue, POC, CA_Questionnaire
from auths.models import CA_Detail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from random import randint
from django.core.validators import RegexValidator, EmailValidator, URLValidator
from auths.models import CA_Detail
from .decorators import profile_required
from django.contrib.auth.models import User
from .choices import STATE_CHOICES

def generateGrievanceId():
        try:
                lpk = Complaints.objects.last().pk+1
        except Exception as e:
                lpk = 1
        return "CX"+str(randint(1563,9874))+str(lpk)

@login_required
@profile_required
def notifications(request):
        all_notifications = Notifications.objects.filter(notification_receiver = request.user)
        sendToAll = User.objects.get(username="sendToAll")
        all_notifications |= Notifications.objects.filter(notification_receiver = sendToAll)
        all_notifications = all_notifications.order_by('-notification_timestamp')[:5]
        return render(request, "ca/notifications.html", {'all_notifications': all_notifications})

@login_required
@profile_required
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
                
                prevQueries = Complaints.objects.filter(user=request.user).order_by('-pk')

                context = {
                'prevQueries': prevQueries,
                'more_active': True,
                }

                return render(request, 'ca/contacts.html', context)


@login_required
@profile_required
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
                
                ideaQueries = Idea.objects.filter(user=request.user).order_by('-pk')

                context = {
                        'ideaQueries': ideaQueries,
                        'idea_active': True,
                }

                return render(request, 'ca/idea.html', context)

@login_required
@profile_required
def faqs(request):
        if request.method == 'POST':
                faq_category = request.POST['faq_category']
                faqs = FAQ.objects.filter(faq_category=faq_category)

                context = {
                'faqs':faqs,
                }

                return render(request, 'ca/faq_response.html', context)

        else:
                return render(request, 'ca/faq.html', {'more_active': True})


@login_required
@profile_required
def venue(request):
        if request.method == 'POST':
                
                data = {}
                if request.POST['venue_name'] == '':
                        data['venue_name'] = "Venue Name Empty"
                
                if request.POST['contact_person'] == '':
                        data['contact_person'] = "Contact Person Empty"
                else:
                        contact_number_validator = RegexValidator('^[0-9]{10}$')
                        try:
                                contact_number_validator(request.POST['contact_number'])
                        except Exception as e:
                                data['contact_number'] = "Contact Number REGEX"



                if request.POST['contact_number'] == '':
                        data['contact_number'] = "Contact Number Empty"

                if request.POST['venue_address'] == '':
                                         data['venue_address'] = "Venue Address Empty"

                
                

                if data:
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
                
                venues = Venue.objects.filter(user=request.user).order_by('-pk')
                name_pattern = "[A-Za-z ]+"
                team_name_pattern = "[A-Za-z0-9, ]+"
                phone_pattern = "[0-9]{10}"

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
                data = {}
                college_name_validator = RegexValidator('^[a-zA-z0-9, ]*$')
                if request.POST['college_name'] == '':
                        data['college_name_stat'] = "COLLEGE NAME EMPTY"
                else:
                        try:
                                college_name_validator(request.POST['college_name'])
                        except Exception as e:
                                data['college_name_stat'] = "COLLEGE NAME REGEX"

                try:
                        alcherid_validator = RegexValidator('^((ALC)-[A-Z]{3}-[0-9]*)?$')
                        alcherid_validator(request.POST['referral'])
                except Exception as e:
                        data['referral_stat'] = "REFERRAL REGEX"
                else:
                        if request.POST['referral'] == request.user.profile.alcher_id:
                                data['referral_stat'] = "ALCHER ID"

                try:
                        college_name_validator(request.POST['por'])
                except Exception as e:
                        data['por_stat'] = "POR REGEX"

                city_validator = RegexValidator('^[a-zA-z0-9,-: ]+$')
                if request.POST['city'] == '':
                        data['city_stat'] = "CITY EMPTY"
                else:
                        try:
                                city_validator(request.POST['city'])
                        except Exception as e:
                                data['city_stat'] = "CITY REGEX"
                                


                if request.POST['mailing_address'] == '':
                        data['mailing_address_stat'] = "MAILING ADDRESS EMPTY"
                else:
                        try:
                                city_validator(request.POST['mailing_address'])
                        except Exception as e:
                                data['mailing_address_stat'] = "MAILING ADDRESS REGEX"

                contact_number_validator = RegexValidator('^[0-9]{10}$')

                if data:
                        college_name = request.POST.get('college_name')
                        city = request.POST.get('city')
                        mailing_address = request.POST.get('mailing_address')
                        # fb = request.POST['fb']
                        por = request.POST.get('por')
                        referral_code = request.POST.get('referral')
                        # full_name = request.POST.get('full_name')
                        state = request.POST.get('state')

                        # print("State: " + state)
                        # print("Full Name" + full_name)
                        
                        # acad=acad
                        # CA_Questionnaire.objects.create(user = request.user, alt_contact=alt_contact,
                        #         college_name=college_name, state=state, city=city, mailing_address=mailing_address, por=por,
                        #         referral_code=referral_code, full_name=full_name, )

                        # CA_Questionnaire.objects.create(user = request.user,
                        #         college_name=college_name, state=state, city=city, mailing_address=mailing_address, por=por,
                        #         referral_code=referral_code, )

                        # ca_det_user = CA_Detail.objects.get(user=request.user)
                        # ca_det_user.ca_profile_complete = True
                        # ca_det_user.save()
                        data['stat'] = "FAILURE"

                        print(data)


                        # print(JsonResponse(data))
                        return redirect('ca:pending')
                        # return JsonResponse(data)

                else:
                        alt_contact = request.POST.get('alt_contact')
                        # acad = request.POST['acad']
                        college_name = request.POST.get('college_name')
                        city = request.POST.get('city')
                        mailing_address = request.POST.get('mailing_address')
                        # fb = request.POST['fb']
                        por = request.POST.get('por')
                        referral_code = request.POST.get('referral')
                        full_name = request.POST.get('full_name')
                        state = request.POST.get('state')
                        # acad=acad
                        # CA_Questionnaire.objects.create(user = request.user, alt_contact=alt_contact,
                        #         college_name=college_name, state=state, city=city, mailing_address=mailing_address, por=por,
                        #         referral_code=referral_code, full_name=full_name, )
                        CA_Questionnaire.objects.create(user = request.user,
                                college_name=college_name, state=state, city=city, mailing_address=mailing_address, por=por,
                                referral_code=referral_code )

                        ca_det_user = CA_Detail.objects.get(user=request.user)
                        ca_det_user.ca_profile_complete = True
                        ca_det_user.save()
                        data['stat'] = "SUCCESS"

                        print(data)
                        # print(JsonResponse(data))
                        return redirect('ca:home')
                        return JsonResponse(data)
                        
        else :
                ca_dets = request.user.ca_details
                if ca_dets.ca_profile_complete and ca_dets.ca_approval :
                        return redirect('ca:home')
                if ca_dets.ca_profile_complete :
                        return redirect('ca:pending')
                context = {
                        'email': request.user.email,
                        'phone_no': request.user.profile.phone,
                        'college': request.user.profile.college,
                        'states': STATE_CHOICES,
                }
                return render(request, 'ca/questionnare.html', context)


@login_required
@profile_required
def home(request):
        return render(request, 'ca/home.html', { 'home_active': True })


@login_required
@profile_required
def guidelines(request):
        
        return render(request, 'ca/guidelines.html', { 'guidelines_active': True })


@login_required
def pending(request):
        ca_dets = request.user.ca_details
        if ca_dets.ca_profile_complete and ca_dets.ca_approval :
                return redirect('ca:home')
        elif not ca_dets.ca_profile_complete :
                return redirect('ca:questionnare')
        return render(request, 'ca/pending.html')


@login_required
@profile_required
def hospitality(request):
        return render(request, 'ca/hospitality.html', {'more_active': True})


@login_required
@profile_required
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
                else:
                        contact_number_validator = RegexValidator('^[0-9]{10}$')
                        try:
                                contact_number_validator(request.POST['poc_phone'])
                        except Exception as e:
                                data['phone'] = "Phone REGEX"


                if request.POST['poc_email'] == '':
                                         data['email'] = "Email Empty"
                else:
                        email_validator = EmailValidator()
                        try:
                                email_validator(request.POST['poc_email'])
                        except Exception as e:
                                data['email'] = "Email REGEX"

                if data:
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
                                name_con=poc_name, desg=poc_designation, phone=poc_phone, email=poc_email, fburl=poc_fb)
                        data['stat'] = "Success"

                        return JsonResponse(data)
        else:
                
                poc_queries = POC.objects.filter(user=request.user)
                context = {
                        'more_active': True,
                        'poc_queries': poc_queries
                }
                return render(request, 'ca/poc.html', context)

@login_required
@profile_required
def standings(request):
        
        idea_count = Idea.objects.filter(user=request.user, approval=1).count()
        poc_count = POC.objects.filter(user=request.user, approval=1).count()
        venue_count = Venue.objects.filter(user=request.user, approval=1).count()
        # share_count = Idea.objects.filter(user=request.user).count()
        referral_count = CA_Questionnaire.objects.filter(referral_code=request.user.profile.alcher_id).count()

        ca_deets = CA_Detail.objects.get(user=request.user)
        # triweekly_score = ca_deets.triweekly
        fbscore = ca_deets.fbscore

        # top5Triweekly = CA_Detail.objects.all().order_by('-triweekly')[:5]
        top10Overall = CA_Detail.objects.all().order_by('-score')[:10]
        # if TriweekyWinner.objects.all().count() > 0:
        #         last_triweekly_winner = TriweekyWinner.objects.all().order_by('-pk')[0]
        # else :
        #         last_triweekly_winner = None
        context = {
                'fbscore':fbscore,
                'idea_count': idea_count,
                'poc_count': poc_count,
                'venue_count': venue_count,
                'referral_count': referral_count,
                # 'triweekly_score': triweekly_score,
                # 'triweekly_standings': top5Triweekly,
                'overall_standings': top10Overall,
                # 'last_triweekly_winner': last_triweekly_winner,
                'more_active': True
        }
        return render(request, 'ca/standings.html', context)
